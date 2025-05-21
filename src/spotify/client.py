from collections.abc import Iterator
from http.client import HTTPResponse
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import logging

from .auth import SpotifyAuth, SpotifyAuthPKCE
from type_definitions import JSONObject
from utils import Cache, user_input


class Spotify:
    BASE_URL: str = "https://api.spotify.com/v1/"
    CONFIRM_DEVICE_PROMPT: str = "Please confirm device to use:"
    MAX_ATTEMPTS: int = 3

    def __init__(self) -> None:
        self._cache: Cache = Cache()
        self._auth_handler: SpotifyAuth = SpotifyAuthPKCE(self.cache)

    @property
    def cache(self) -> Cache:
        return self._cache

    @property
    def auth_handler(self) -> SpotifyAuth:
        return self._auth_handler

    def get_access_token(self) -> None:
        self._access_token: str = self.auth_handler.get_access_token()

    @staticmethod
    def _url(suffix: str, parameters: JSONObject | None = None) -> str:
        url: str = f"{Spotify.BASE_URL}{suffix}"
        if parameters is None:
            return url
        return f"{url}?{urlencode(parameters)}"

    def _request(
        self,
        method: str,
        url: str,
        parameters: JSONObject | None = None,
        data: bytes | str | None = None,
        attempts: int = 0,
    ) -> bytes:
        if attempts == Spotify.MAX_ATTEMPTS:
            raise Exception(f"Reached max attempts for {method} {url}")
        if not hasattr(self, "_access_token"):
            self.get_access_token()
        logging.debug(f"Sending {method} request to {url} with {data}")
        request: Request = Request(
            method=method,
            url=Spotify._url(url, parameters),
            data=data.encode() if isinstance(data, str) else data,
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        response: HTTPResponse = urlopen(request)
        if response.status == 403:
            logging.debug("403 response from {url}, refreshing access token")
            self.get_access_token()
            return self._request(method, url, attempts=attempts + 1)
        return response.read()

    def get_top(
        self,
        item_type: str,
        term: str = "medium_term",
        limit: int = 20,
        offset: int = 0,
    ) -> Iterator[tuple[int, JSONObject]]:
        method: str = "GET"
        url: str = f"me/top/{item_type}"
        parameters: dict[str, str | int] = {
            "time_range": term,
            "limit": limit,
            "offset": offset,
        }
        response: bytes = self._request(method, url, parameters)
        tracks: JSONObject = json.loads(response)
        rank: int = offset + 1
        for n, item in enumerate(tracks["items"]):
            yield rank + n, item

    def get_saved_tracks(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> Iterator[JSONObject]:
        method: str = "GET"
        url: str = "me/tracks"
        parameters: dict[str, int] = {"limit": limit, "offset": offset}
        response: bytes = self._request(method, url, parameters)
        yield from json.loads(response)["items"]

    def get_devices(self) -> Iterator[JSONObject]:
        method: str = "GET"
        url: str = "me/player/devices"
        response: bytes = self._request(method, url)
        yield from json.loads(response)["devices"]

    def _get_device_id(self, device_id: str | None = None) -> str:
        if device_id is not None:
            return device_id
        devices: dict[str, tuple[str, str]] = {}
        for n, device in enumerate(self.get_devices()):
            if device["is_active"]:
                return device["id"]
            devices[str(n)] = device["name"], device["id"]
        n_devices: int = len(devices)
        digits: int = len(str(n_devices))
        for n, device in devices.items():
            print(f"{int(n):{digits}d}", device[0])
        device_n: str = user_input(
            prompt=Spotify.CONFIRM_DEVICE_PROMPT,
            options=list(devices.keys()),
        )
        return devices[device_n][1]

    def previous(self, device_id: str | None = None) -> bytes:
        method: str = "POST"
        url: str = "me/player/previous"
        parameters: dict[str, str] = {
            "device_id": self._get_device_id(device_id),
        }
        return self._request(method, url, parameters)

    def next(self, device_id: str | None = None) -> bytes:
        method: str = "POST"
        url: str = "me/player/next"
        parameters: dict[str, str] = {
            "device_id": self._get_device_id(device_id),
        }
        return self._request(method, url, parameters)
