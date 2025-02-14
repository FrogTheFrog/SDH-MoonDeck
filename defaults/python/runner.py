# autopep8: off
def get_plugin_dir():
    from pathlib import Path
    return Path(__file__).parent.resolve()

def add_plugin_to_path():
    import sys

    plugin_dir = get_plugin_dir()
    directories = [["./"], ["lib"], ["externals"]]
    for dir in directories:
        sys.path.append(str(plugin_dir.joinpath(*dir)))

add_plugin_to_path()

from enum import Enum
from typing import Optional, TypedDict
from lib.moonlightproxy import MoonlightProxy, ResolutionDimensions
from lib.buddyrequests import AppState, HostInfoResponse, ResultLikeResponse, StreamState, StreamStateResponse, StreamedAppDataResponse
from lib.buddyclient import BuddyClient, HelloResult
from lib.logger import logger, set_log_filename, enable_debug_level
from lib.settings import Dimension, HostSettings, settings_manager, RunnerTimeouts
from lib.wolsplashscreen import WolSplashScreen
from lib.runner.settingsparser import parse_settings

import os
import asyncio
import lib.constants as constants
import lib.hostinfo as hostinfo
import lib.runnerresult as runnerresult
# autopep8: on

set_log_filename(constants.RUNNER_LOG_FILE, rotate=False)





async def sleep_before_return_if_false(value):
    if value is False:
        await asyncio.sleep(1)
    return value


async def pool_async(predicate, *requests):
    assert len(requests) > 0
    while True:
        responses = [await request() for request in requests]
        for response in responses:
            if not isinstance(response, dict):
                return response

        result = await predicate(*responses)
        if isinstance(result, bool) or result is None:
            if result:
                return None
        else:
            return result


async def sleep_while_counting_down(object_ref, error: runnerresult.Result):
    object_ref["retries"] -= 1
    if object_ref["retries"] > 0:
        return await sleep_before_return_if_false(False)
    else:
        return error


async def wait_for_app_to_close(client: BuddyClient, app_id: int):
    async def wait_till_close(info: HostInfoResponse):
        if info["steamRunningAppId"] != app_id or not info["steamIsRunning"]:
            return True

        await asyncio.sleep(1)

    return await pool_host_info(client, wait_till_close)


async def wait_for_stream_to_stop(client: BuddyClient, timeouts: RunnerTimeouts):
    obj = {"retries": timeouts["streamEnd"]}
    if obj["retries"] <= 0:
        return None

    async def wait_to_stop(info: HostInfoResponse):
        if info["streamState"] == StreamState.NotStreaming:
            return True

        return await sleep_while_counting_down(obj, runnerresult.Result.StreamDidNotEnd)

    return await pool_host_info(client, wait_to_stop)


async def wait_for_app_launch(client: BuddyClient, app_id: int, timeouts: RunnerTimeouts):
    obj = {"retries": timeouts["appLaunch"], "stability_counter": timeouts["appLaunchStability"]}

    async def wait_till_launch(app: StreamedAppDataResponse):
        data = app["data"]
        if data is None:
            return runnerresult.Result.AppLaunchAborted
        
        state = data["state"]
        if state == AppState.Running:
            return True
        
        

        if info["steamIsRunning"]:
            if info["steamRunningAppId"] == app_id:
                # Reset the retry counter to the initial value for even more stability...
                obj["retries"] = timeouts["appLaunch"]

                # Counter is needed for apps that come with brain-dead launcher (EALink for example)
                obj["stability_counter"] -= 1

                # Usual the Steam app state changes rapidly with launchers, so if it stays
                # consistent for like 15s, it should be good enough for us
                return await sleep_before_return_if_false(obj["stability_counter"] == 0)
            else:
                # See note above, we are want the app id to stay consistent for 10s
                obj["stability_counter"] = timeouts["appLaunchStability"]

                if info["steamTrackedUpdatingAppId"] == app_id:
                    obj["was_updating"] = True
                    return await sleep_before_return_if_false(False)
                elif obj["was_updating"]:
                    # If the app is no longer updating we need to re-launch it by
                    # returning this special value
                    return SpecialHandling.AppFinishedUpdating

        return await sleep_while_counting_down(obj, runnerresult.Result.AppLaunchFailed)

    return await pool_async(wait_till_launch, client.get_streamed_app_data)


async def wait_for_steam_to_be_ready(client: BuddyClient, timeouts: RunnerTimeouts):
    obj = {"retries": timeouts["steamReadiness"]}

    async def wait_till_steam_is_ready(response: ResultLikeResponse):
        if response["result"]:
            return True

        return await sleep_while_counting_down(obj, runnerresult.Result.SteamDidNotReadyUpInTime)

    return await pool_async(wait_till_steam_is_ready, client.is_steam_ready)


async def wait_for_stream_to_be_ready(client: BuddyClient, timeouts: RunnerTimeouts):
    obj = {"retries": timeouts["streamReadiness"]}

    async def wait_till_stream_is_ready(stream_state: StreamStateResponse):
        if stream_state["state"] == StreamState.Streaming:
            return True

        return await sleep_while_counting_down(obj, runnerresult.Result.StreamFailedToStart)

    return await pool_async(wait_till_stream_is_ready, client.get_stream_state)


async def launch_app_and_wait(client: BuddyClient, app_id: int, timeouts: RunnerTimeouts):
    logger.info("Waiting for Buddy to be ready to launch games")
    result = await wait_for_stream_to_be_ready(client, timeouts)
    if result:
        return result

    logger.info(f"Sending request to launch app {app_id}")
    result = await client.launch_app(app_id)
    if result:
        return result
    
    logger.info(f"Waiting for Steam to be ready")
    result = await wait_for_steam_to_be_ready(client, timeouts)
    if result:
        return result

    logger.info(f"Waiting for app {app_id} to be launched in Steam")
    result = await wait_for_app_launch(client, app_id, timeouts)
    if result:
        return result

    # retries = timeouts["appUpdate"]
    # result = SpecialHandling.AppFinishedUpdating
    # while result == SpecialHandling.AppFinishedUpdating and retries:
    #     retries -= 1

    #     logger.info(f"Sending request to launch app {app_id}")
    #     result = await client.launch_app(app_id)
    #     if result:
    #         return result

    #     logger.info(f"Waiting for app {app_id} to be launched in Steam")
    #     result = await wait_for_app_launch(client, app_id, timeouts)
    #     if result and result != SpecialHandling.AppFinishedUpdating:
    #         return result 

    # if result:
    #     logger.info(f"Giving up waiting for {app_id} to finish updating cycles")
    #     return result    

    logger.info("Waiting for app or Steam to close")
    result = await wait_for_app_to_close(client, app_id)
    if result:
        return result


async def start_moonlight(proxy: MoonlightProxy):
    logger.info("Checking if Moonlight flatpak is installed or custom binary exists")
    if not await proxy.is_moonlight_installed():
        return runnerresult.Result.MoonlightIsNotInstalled

    logger.info("Terminating all Moonlight instances if any")
    await proxy.terminate_all_instances(kill_all=True)

    logger.info("Starting Moonlight")
    await proxy.start()


async def wait_for_initial_host_conditions(client: BuddyClient, app_id: int, timeouts: RunnerTimeouts):
    obj = {"retries": timeouts["initialConditions"]}

    async def wait_till_stream_is_ready(stream_state: StreamStateResponse, app: StreamedAppDataResponse):
        if stream_state["state"] == StreamState.StreamEnding:
            return await sleep_while_counting_down(obj, runnerresult.Result.StreamDidNotEnd)

        if stream_state["state"] == StreamState.Streaming:
            data = app["data"]
            if data is None:
                # Stream is active, but the app was not started for some reason
                return True
            
            if data["app_id"] == app_id:
                # Already streaming this very app
                return True

            return await sleep_while_counting_down(obj, runnerresult.Result.AnotherSteamAppIsStreaming)

        return True

    logger.info("Waiting for a initial stream conditions to be satisfied")
    result = await pool_async(wait_till_stream_is_ready, client.get_stream_state, client.get_streamed_app_data)
    if result:
        return result

    return None


async def establish_connection(client: BuddyClient, mac: str, hostInfoPort: int, timeouts: RunnerTimeouts):
    logger.info("Checking connection to Buddy and GameStream server")

    async with WolSplashScreen(client.address, mac, timeouts["wakeOnLan"]) as splash:
        while True:
            buddy_result = await client.say_hello(force=True)
            if buddy_result:
                if buddy_result != HelloResult.Offline:
                    return buddy_result
            
            buddy_status = buddy_result != HelloResult.Offline
            server_status = await hostinfo.get_server_info(client.address, 
                                                           hostInfoPort, 
                                                           timeout=timeouts["servicePing"]) is not None
            
            if not splash.update(buddy_status, server_status):
                if not buddy_status:
                    return HelloResult.Offline
                if not server_status:
                    return runnerresult.Result.GameStreamDead
                return None


async def end_the_stream(client: BuddyClient, close_steam: bool, timeouts: RunnerTimeouts):
    logger.info("App closed gracefully, ending stream if it's still open")
    result = await client.end_stream()
    if result:
        return result

    if close_steam:
        logger.info("Asking to close Steam if it's still open")
        result = await client.close_steam()
        if result:
            return result
        
    logger.info("Waiting for stream to stop")
    result = await wait_for_stream_to_stop(client, timeouts)
    if result:
        return result


async def run_game(res_change: ResolutionChange, host_app: str, hostname: str, mac: str, address: str, hostInfoPort:int, buddyPort: int, client_id: Optional[str], close_steam: bool, timeouts: RunnerTimeouts, moonlight_exec_path: Optional[str], app_id: int):
    try:
        async with BuddyClient(address, buddyPort, client_id, timeouts["buddyRequests"]) as client, \
                   MoonlightProxy(hostname, host_app, res_change["dimensions"] if res_change["passToMoonlight"] else None, moonlight_exec_path) as proxy:
            result = await establish_connection(client=client, mac=mac, hostInfoPort=hostInfoPort, timeouts=timeouts)
            if result:
                return result

            result = await wait_for_initial_host_conditions(res_change=res_change, client=client, app_id=app_id, timeouts=timeouts)
            if result:
                return result

            result = await start_moonlight(proxy=proxy)
            if result:
                return result

            proxy_task = asyncio.create_task(proxy.wait())
            launch_task = asyncio.create_task(launch_app_and_wait(client=client, app_id=app_id, timeouts=timeouts))

            done, _ = await asyncio.wait({proxy_task, launch_task}, return_when=asyncio.FIRST_COMPLETED)
            if proxy_task in done:
                done, _ = await asyncio.wait({launch_task}, timeout=2)
                if launch_task in done:
                    result = launch_task.result()
                    if result:
                        return result
                else:
                    launch_task.cancel()
                    await asyncio.wait({launch_task}, timeout=2)
                    return runnerresult.Result.MoonlightClosed
            else:
                assert launch_task in done, "Launch task is not done?!"  

                logger.info("Ending stream") 
                result = await client.end_stream()
                if result:
                    logger.error(f"Failed to end the stream: {result.value}")

                result = launch_task.result()
                if result:
                    return result
                
            result = await end_the_stream(client=client, close_steam=close_steam, timeouts=timeouts)
            if result:
                return result

    except Exception:
        logger.exception("Unhandled exception")
        return runnerresult.Result.Exception










async def main():
    try:
        logger.info("Resetting runner result")
        runnerresult.set_result(runnerresult.Result.ClosedPrematurely, log_result=False)

        logger.info("Parsing runner settings")
        settings = await parse_settings()

        if settings["debug_logs"]:
            enable_debug_level()

        
        result = await run_game(res_change,
                                host_app,
                                host_settings["hostName"],
                                host_settings["mac"],
                                host_settings["address"],
                                host_settings["hostInfoPort"],
                                host_settings["buddyPort"],
                                user_settings["clientId"],
                                host_settings["closeSteamOnceSessionEnds"],
                                host_settings["runnerTimeouts"],
                                user_settings["moonlightExecPath"] if user_settings["useMoonlightExec"] else None,
                                app_id)
        runnerresult.set_result(result)

    except runnerresult.RunnerError as err:
        runnerresult.set_result(err.result)

    except Exception:
        logger.exception("Unhandled exception")
        runnerresult.set_result(runnerresult.Result.Exception)


if __name__ == "__main__":
    asyncio.run(main())
