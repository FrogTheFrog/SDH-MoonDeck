import aiohttp
import base64
import contextlib
import pathlib
import ssl
from . import utils

from typing import List, Optional, TypedDict
from enum import Enum


class PairingState(Enum):
    Paired = 0
    Pairing = 1
    NotPaired = 2


class PcState(Enum):
    Normal = 0
    Restarting = 1
    ShuttingDown = 2
    Suspending = 3


class PcStateChange(Enum):
    Restart = 0
    Shutdown = 1
    Suspend = 2


class StreamState(Enum):
    NotStreaming = 0
    Streaming = 1
    StreamEnding = 2


class ApiVersionResponse(TypedDict):
    version: int


class PairingStateResponse(TypedDict):
    state: PairingState


class PcStateResponse(TypedDict):
    state: PcState


class ResultLikeResponse(TypedDict):
    result: bool


class GamestreamAppNamesResponse(TypedDict):
    appNames: Optional[List[str]]


class HostInfoResponse(TypedDict):
    steamIsRunning: bool
    steamRunningAppId: int
    steamTrackedUpdatingAppId: Optional[int]
    streamState: StreamState


class BuddyRequests(contextlib.AbstractAsyncContextManager):

    def __init__(self, address: str, port: int, client_id: str, timeout: float) -> None:
        super().__init__()
        self.base_url = f"https://{address}:{port}"
        self.client_id = client_id
        self.timeout = timeout
        self.__session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        headers = {"authorization": f"basic {base64.b64encode(self.client_id.encode('utf-8')).decode('utf-8')}"}

        cafile = str(pathlib.Path(__file__).parent.resolve().joinpath("..", "ssl", "moondeck_cert.pem"))
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
        ssl_context.check_hostname = False
        connector = aiohttp.TCPConnector(ssl=ssl_context)

        self.__session = await aiohttp.ClientSession(
            timeout=timeout, 
            raise_for_status=True, 
            headers=headers,
            connector=connector
        ).__aenter__()
        return self

    async def __aexit__(self, *args):
        session = self.__session
        self.__session = None
        return await session.__aexit__(*args)

    async def get_api_version(self):
        async with self.__session.get(f"{self.base_url}/apiVersion") as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ApiVersionResponse, data)

    async def get_pairing_state(self):
        async with self.__session.get(f"{self.base_url}/pairingState/{self.client_id}") as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(PairingStateResponse, data)

    async def post_start_pairing(self, pin: int):
        data = {
            "id": self.client_id,
            "hashed_id": base64.b64encode((self.client_id + str(pin)).encode("utf-8")).decode("utf-8")
        }

        async with self.__session.post(f"{self.base_url}/pair", json=data) as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)

    async def post_abort_pairing(self):
        data = {
            "id": self.client_id
        }

        async with self.__session.post(f"{self.base_url}/abortPairing", json=data) as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)

    async def post_launch_steam_app(self, app_id: int):
        data = {
            "app_id": app_id
        }

        async with self.__session.post(f"{self.base_url}/launchSteamApp", json=data) as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)

    async def post_close_steam(self, grace_period: Optional[int]):
        data = {
            "grace_period": grace_period
        }

        async with self.__session.post(f"{self.base_url}/closeSteam", json=data) as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)

    async def get_pc_state(self):
        async with self.__session.get(f"{self.base_url}/pcState") as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(PcStateResponse, data)

    async def post_change_pc_state(self, state: PcStateChange, grace_period: int):
        data = {
            "state": state.name,
            "grace_period": grace_period
        }

        async with self.__session.post(f"{self.base_url}/changePcState", json=data) as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)

    async def post_change_resolution(self, width: int, height: int, manual: bool):
        data = {
            "width": width,
            "height": height,
            "manual": manual
        }

        async with self.__session.post(f"{self.base_url}/changeResolution", json=data) as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)
        
    async def post_restore_resolution(self, manual: bool):
        data = {
            "manual": manual
        }

        async with self.__session.post(f"{self.base_url}/restoreResolution", json=data) as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)

    async def get_host_info(self):
        async with self.__session.get(f"{self.base_url}/hostInfo") as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(HostInfoResponse, data)

    async def post_end_stream(self):
        async with self.__session.post(f"{self.base_url}/endStream") as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(ResultLikeResponse, data)

    async def get_gamestream_app_names(self):
        async with self.__session.get(f"{self.base_url}/gamestreamAppNames") as resp:
            data = await resp.json(encoding="utf-8")
            return utils.from_dict(GamestreamAppNamesResponse, data)
