import os
from . import constants

from enum import Enum
from typing import Optional
from .logger import logger


class Result(Enum):
    ClosedPrematurely = "MoonDeck runner closed prematurely!"
    NoAppId = "Failed to parse app id!"
    HostNotSelected = "Host is not selected!"
    Exception = "Unhandled exception!"
    GameStreamDead = "GameStream service not responsing!"
    AnotherSteamAppIsStreaming = "Another Steam App is streaming!"
    StreamFailedToStart = "Stream failed to start!"
    SteamDidNotReadyUpInTime = "Steam did not reach the \"ready\" state in time!"
    StreamDidNotEnd = "Stream did not end in time!"
    AppLaunchAborted = "App launch was aborted!"
    AppLaunchFailed = "Failed to launch app in time!"
    MoonlightClosed = "Moonlight has been closed!"
    MoonlightIsNotInstalled = "Moonlight executable/flatpak not found!"


class RunnerError(Exception):
    def __init__(self, result: Enum):
        super().__init__(result.value)
        self.result = result


def set_result(result: Optional[Enum], log_result=True):
    try:
        if result:
            assert isinstance(result.value, str), f"{result.value} is not a string!"
            with open(constants.RUNNER_RESULT_FILE, "w+") as file:
                file.write(result.value)
                if log_result:
                    logger.error(result.value)
        else:
            if os.path.exists(constants.RUNNER_RESULT_FILE):
                os.remove(constants.RUNNER_RESULT_FILE)
    except Exception:
        logger.exception("Unhandled exception")


def get_result():
    try:
        if os.path.exists(constants.RUNNER_RESULT_FILE):
            with open(constants.RUNNER_RESULT_FILE, "r") as file:
                return file.readline()

        return None
    except Exception:
        logger.exception("Unhandled exception")
        return "Expection while checking result!"
