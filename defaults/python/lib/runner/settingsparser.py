import os

from typing import Optional, TypedDict

from .envparser import EnvSettings, parse_env_settings
from ..runnerresult import RunnerError, Result
from ..settings import Dimension, HostSettings, RunnerTimeouts, settings_manager
from ..moonlightproxy import ResolutionDimensions
from ..logger import logger


class ResolutionSettings(TypedDict):
    dimensions: ResolutionDimensions
    pass_to_moonlight: bool


class RunnerSettings(TypedDict):
    resolution: ResolutionSettings
    host_app: str
    hostname: str
    mac: str
    address: str
    host_port:int
    buddy_port: int
    client_id: str
    close_steam: bool
    timeouts: RunnerTimeouts
    moonlight_exec_path: Optional[str]
    app_id: int
    debug_logs: bool


def parse_resolution_settings(host_settings: HostSettings, env_settings: EnvSettings) -> ResolutionSettings:
    dimensions: ResolutionDimensions = { 
        "size": None,
        "bitrate": host_settings["resolution"]["defaultBitrate"],
        "fps": host_settings["resolution"]["defaultFps"]
    }
    dimension_list = host_settings["resolution"]["dimensions"]

    def update_dimensions(dimension: Dimension):
        dimensions["size"] = { "width": dimension["width"], "height": dimension["height"] }
        if dimension["bitrate"] is not None:
            dimensions["bitrate"] = dimension["bitrate"]
        if dimension["fps"] is not None:
            dimensions["fps"] = dimension["fps"]

    if host_settings["resolution"]["useLinkedDisplays"] and len(dimension_list) > 0:
        linked_display = env_settings["linked_display"]
        if linked_display:
            for dimension in dimension_list:
                if linked_display in dimension["linkedDisplays"]:
                    logger.info(f"Using linked custom resolution for display \"{linked_display}\".")
                    update_dimensions(dimension)

    if not dimensions["size"] and host_settings["resolution"]["useCustomDimensions"] and len(dimension_list) > 0:
        index = host_settings["resolution"]["selectedDimensionIndex"]
        if index >= 0 and index < len(dimension_list):
            logger.info("Using custom resolution.")
            update_dimensions(dimension_list[index])
        else:
            logger.warn(f"Dimension index ({index}) out of range ([0;{len(dimension_list)}]). Still continuing...")
    
    if not dimensions["size"] and host_settings["resolution"]["automatic"]:
        auto_resolution = env_settings["auto_resolution"]
            
        logger.info(f"Using auto resolution from MoonDeck: {auto_resolution}")
        if auto_resolution:
            dimensions["size"] = { "width": auto_resolution["width"], "height": auto_resolution["height"] }
        else:
            logger.warning(f"Cannot use automatic resolution! MoonDeck did not pass resolution. Still continuing...")
        
    res_change: ResolutionSettings = { 
        "dimensions": dimensions,
        "pass_to_moonlight": host_settings["resolution"]["passToMoonlight"]
    }
    logger.info(f"Parsed resolution settings: {res_change}")
    return res_change

def parse_host_app_name(host_settings: HostSettings) -> str:
    host_app: str = "MoonDeckStream"
    app_list = host_settings["hostApp"]["apps"]
    if len(app_list) > 0:
        index = host_settings["hostApp"]["selectedAppIndex"]
        if index >= 0 and index < len(app_list):
            host_app = app_list[index]
        else:
            logger.warning(f"Host app index ({index}) out of range ([0;{len(app_list)}]). Still continuing...")
    
    logger.info(f"Parsed host app name: {host_app}")
    return host_app


async def parse_settings() -> RunnerSettings:
    logger.info("Getting current host settings")
    user_settings = await settings_manager.get()
    host_settings = None

    host_id = user_settings["currentHostId"]
    if host_id is not None and host_id in user_settings["hostSettings"]:
        host_settings = user_settings["hostSettings"][host_id]

    if host_settings is None:
        raise RunnerError(Result.HostNotSelected)

    logger.info("Parsing ENV settings")
    env_settings = parse_env_settings()

    if env_settings["app_id"] is None:
        raise RunnerError(Result.NoAppId)                        

    return {
        "resolution": parse_resolution_settings(),
        "host_app": parse_host_app_name(),
        "hostname": host_settings["hostName"],
        "mac": host_settings["mac"],
        "address": host_settings["address"],
        "host_port": host_settings["hostInfoPort"],
        "buddy_port": host_settings["buddyPort"],
        "client_id": user_settings["clientId"],
        "close_steam": host_settings["closeSteamOnceSessionEnds"],
        "timeouts": host_settings["runnerTimeouts"],
        "moonlight_exec_path": user_settings["moonlightExecPath"] if user_settings["useMoonlightExec"] else None,
        "app_id": env_settings["app_id"],
        "debug_logs": user_settings["runnerDebugLogs"]
    }
