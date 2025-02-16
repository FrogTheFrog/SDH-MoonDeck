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

from lib.runner.moondeckapprunner import MoonDeckAppRunner
from lib.logger import logger, set_log_filename, enable_debug_level
from lib.runner.settingsparser import parse_settings

import asyncio
import lib.constants as constants
import lib.runnerresult as runnerresult
# autopep8: on

set_log_filename(constants.RUNNER_LOG_FILE, rotate=False)

async def main():
    try:
        logger.info("Resetting runner result")
        runnerresult.set_result(runnerresult.Result.ClosedPrematurely, log_result=False)

        logger.info("Parsing runner settings")
        settings = await parse_settings()

        if settings["debug_logs"]:
            enable_debug_level()
        
        await MoonDeckAppRunner.run(settings)

    except runnerresult.RunnerError as err:
        runnerresult.set_result(err.result)

    except Exception:
        logger.exception("Unhandled exception")
        runnerresult.set_result(runnerresult.Result.Exception)


if __name__ == "__main__":
    asyncio.run(main())
