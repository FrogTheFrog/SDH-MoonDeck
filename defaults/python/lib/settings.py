import pathlib
import uuid
import copy
import json
from . import constants
from . import utils

from typing import Any, Dict, List, Literal, Optional, TypedDict, get_args
from .logger import logger
from .buddyrequests import OsType


ControllerConfigOption = Literal["Disable", "Default", "Enable", "Noop"]


class RunnerTimeouts(TypedDict):
    buddyRequests: int
    servicePing: int
    initialConditions: int
    streamReadiness: int
    steamReadiness: int
    appLaunch: int
    appLaunchStability: int
    streamEnd: int
    wakeOnLan: int
    steamLaunch: int
    steamLaunchAfterSuspend: int
    networkReconnectAfterSuspend: int


class HostApp(TypedDict):
    selectedAppIndex: int
    apps: List[str]


class Dimension(TypedDict):
    width: int
    height: int
    bitrate: Optional[int]
    fps: Optional[int]
    linkedDisplays: List[str]


class HostResolution(TypedDict):
    automatic: bool
    appResolutionOverride: Literal["CustomResolution", "DisplayResolution", "Native", "Default"]
    passToBuddy: bool
    passToMoonlight: bool
    useCustomDimensions: bool
    useLinkedDisplays: bool
    selectedDimensionIndex: int
    defaultBitrate: Optional[int]
    defaultFps: Optional[int]
    dimensions: List[Dimension]


class SunshineAppsSettings(TypedDict):
    showQuickAccessButton: bool
    lastSelectedOverride: str
    lastSelectedControllerConfig: ControllerConfigOption


class HostSettings(TypedDict):
    hostInfoPort: int
    buddyPort: int
    address: str
    staticAddress: bool
    hostName: str
    mac: str
    os: OsType
    closeSteamOnceSessionEnds: bool
    resolution: HostResolution
    hostApp: HostApp
    runnerTimeouts: RunnerTimeouts
    sunshineApps: SunshineAppsSettings


class GameSessionSettings(TypedDict):
    autoApplyAppId: bool
    resumeAfterSuspend: bool
    controllerConfig: ControllerConfigOption


class ButtonPositionSettings(TypedDict):
    horizontalAlignment: Literal["top", "bottom"]
    verticalAlignment: Literal["left", "right"]
    offsetX: str
    offsetY: str
    offsetForHltb: bool
    zIndex: str


class ButtonStyleSettings(TypedDict):
    showFocusRing: bool
    theme: Literal["HighContrast", "Clean"]


class UserSettings(TypedDict):
    version: constants.CONFIG_VERSION_LITERAL
    clientId: str
    currentHostId: Optional[str]
    gameSession: GameSessionSettings
    buttonPosition: ButtonPositionSettings
    buttonStyle: ButtonStyleSettings
    enableMoondeckShortcuts: bool
    enableMoondeckButtonPrompt: bool
    hostSettings: Dict[str, HostSettings]
    runnerDebugLogs: bool
    useMoonlightExec: bool
    moonlightExecPath: str
    pythonExecPath: str


class SettingsManager:
    async def get(self):
        settings: Optional[UserSettings] = None
        try:
            with open(f"{constants.CONFIG_DIR}/{constants.CONFIG_FILENAME}", "r") as file:
                data: Dict[str, Any] = json.load(file)
                try:
                    settings = utils.from_dict(UserSettings, data)
                except Exception:
                    try:
                        if not settings:
                            settings = utils.from_dict(UserSettings, self._migrate_settings(data))
                            await self.set(settings)
                    except Exception:
                        logger.exception("failed to parse user settings")
                        

        except FileNotFoundError:
            pass
        except Exception:
            logger.exception("failed to load settings")
            pass

        if settings:
            return settings
        else:
            return await self.set(utils.from_dict(UserSettings, {
                "version": get_args(constants.CONFIG_VERSION_LITERAL)[0],
                "clientId": str(uuid.uuid4()),
                "currentHostId": None,
                "gameSession": {
                    "autoApplyAppId": False,
                    "resumeAfterSuspend": False,
                    "controllerConfig": "Noop"
                },
                "buttonPosition": {
                    "horizontalAlignment": "bottom",
                    "verticalAlignment": "right",
                    "offsetX": "",
                    "offsetY": "",
                    "offsetForHltb": False,
                    "zIndex": ""
                },
                "buttonStyle": {
                    "showFocusRing": True,
                    "theme": "Clean"
                },
                "enableMoondeckShortcuts": True,
                "enableMoondeckButtonPrompt": False,
                "hostSettings": {},
                "runnerDebugLogs": False,
                "useMoonlightExec": False,
                "moonlightExecPath": "",
                "pythonExecPath": ""}))

    async def set(self, settings: UserSettings):
        try:
            pathlib.Path(constants.CONFIG_DIR).mkdir(
                parents=True, exist_ok=True)
            with open(f"{constants.CONFIG_DIR}/{constants.CONFIG_FILENAME}", "w") as file:
                json.dump(settings, file,
                          ensure_ascii=False, allow_nan=False,
                          indent=4)
        except Exception:
            logger.exception("failed to save settings")

        self.__data = copy.deepcopy(settings)
        return copy.deepcopy(self.__data)

    @staticmethod
    def _migrate_settings(data: Dict[str, Any]) -> Dict[str, Any]:
        if data["version"] == 1:
            data["version"] = 2
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["resolution"] = {
                    "automatic": True,
                    "earlyChangeEnabled": True,
                    "passToMoonlight": True,
                    "useCustomDimensions": False,
                    "customWidth": 1280,
                    "customHeight": 800
                }
        if data["version"] == 2:
            data["version"] = 3
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["staticAddress"] = False
        if data["version"] == 3:
            data["version"] = 4
            for host in data["hostSettings"].keys():
                del data["hostSettings"][host]["resolution"]["customWidth"]
                del data["hostSettings"][host]["resolution"]["customHeight"]
                data["hostSettings"][host]["resolution"]["selectedDimensionIndex"] = -1
                data["hostSettings"][host]["resolution"]["dimensions"] = []
        if data["version"] == 4:
            data["version"] = 5
            for host in data["hostSettings"].keys():
                del data["hostSettings"][host]["resolution"]["earlyChangeEnabled"]
        if data["version"] == 5:
            data["version"] = 6
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["closeSteamOnceSessionEnds"] = False
        if data["version"] == 6:
            data["version"] = 7
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["resolution"]["defaultBitrate"] = None
                for i in range(len(data["hostSettings"][host]["resolution"]["dimensions"])):
                    data["hostSettings"][host]["resolution"]["dimensions"][i]["bitrate"] = None
        if data["version"] == 7:
            data["version"] = 8
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["hostApp"] = { "selectedAppIndex": -1, "apps": [] }
        if data["version"] == 8:
            data["version"] = 9
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["resolution"]["appResolutionOverride"] = "CustomResolution"
        if data["version"] == 9:
            data["version"] = 10
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["resolution"]["passToBuddy"] = True
        if data["version"] == 10:
            data["version"] = 11
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["hostInfoPort"] = 47989
        if data["version"] == 11:
            data["version"] = 12
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["runnerTimeouts"] = { "buddyRequests": 5, "servicePing": 5, "initialConditions": 30, "streamReadiness": 30, "appLaunch": 30, "appLaunchStability": 15, "appUpdate": 5 }
                data["hostSettings"][host]["runnerDebugLogs"] = False
                data["hostSettings"][host]["resolution"]["defaultFps"] = None
                for i in range(len(data["hostSettings"][host]["resolution"]["dimensions"])):
                    data["hostSettings"][host]["resolution"]["dimensions"][i]["fps"] = None
        if data["version"] == 12:
            data["version"] = 13
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["runnerTimeouts"]["streamEnd"] = 15
        if data["version"] == 13:
            data["version"] = 14
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["resolution"]["useLinkedDisplays"] = True
                for i in range(len(data["hostSettings"][host]["resolution"]["dimensions"])):
                    data["hostSettings"][host]["resolution"]["dimensions"][i]["linkedDisplays"] = []
        if data["version"] == 14:
            data["version"] = 15
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["runnerTimeouts"]["wakeOnLan"] = 60
        if data["version"] == 15:
            data["version"] = 16
            for host in data["hostSettings"].keys():
                del data["hostSettings"][host]["runnerDebugLogs"]
            
            data["runnerDebugLogs"] = False
            data["useMoonlightExec"] = False
            data["moonlightExecPath"] = ""
        if data["version"] == 16:
            data["version"] = 17
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["os"] = "Other"
        if data["version"] == 17:
            data["version"] = 18
            data["buttonPosition"]["zIndex"] = ""
        if data["version"] == 18:
            data["version"] = 19
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["sunshineApps"] = { "showQuickAccessButton": False, "lastSelectedOverride": "Default" }
        if data["version"] == 19:
            data["version"] = 20
            data["enableMoondeckShortcuts"] = True
        if data["version"] == 20:
            data["version"] = 21
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["runnerTimeouts"]["steamLaunch"] = 5
                data["hostSettings"][host]["runnerTimeouts"]["steamLaunchAfterSuspend"] = 15
                data["hostSettings"][host]["runnerTimeouts"]["networkReconnectAfterSuspend"] = 15
        if data["version"] == 21:
            data["version"] = 22
            data["enableMoondeckButtonPrompt"] = False
        if data["version"] == 22:
            data["version"] = 23
            data["gameSession"]["controllerConfig"] = "Noop"
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["sunshineApps"]["lastSelectedControllerConfig"] = "Noop"
        if data["version"] == 23:
            data["version"] = 24
            data["pythonExecPath"] = ""
        if data["version"] == 24:
            data["version"] = 25
            for host in data["hostSettings"].keys():
                if data["hostSettings"][host]["os"] == "Windows":
                    data["hostSettings"][host]["resolution"]["passToBuddy"] = False
        if data["version"] == 25:
            data["version"] = 26
            for host in data["hostSettings"].keys():
                data["hostSettings"][host]["runnerTimeouts"]["steamReadiness"] = 60
                del data["hostSettings"][host]["runnerTimeouts"]["appUpdate"]
                del data["hostSettings"][host]["resolution"]["passToBuddy"]
        return data


settings_manager = SettingsManager()
