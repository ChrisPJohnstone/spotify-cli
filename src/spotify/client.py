from collections.abc import Iterator
from http.client import HTTPResponse
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import logging

from .auth import AuthPKCE
from type_definitions import JSONObject
from utils import Cache


class Spotify:
    CLIENT_ID: str = "b37fc55dfdd8409db2411464ba60ef5e"
    BASE_URL: str = "https://api.spotify.com/v1/"
    MAX_ATTEMPTS: int = 3

    def __init__(self) -> None:
        self._cache: Cache = Cache()
        self._auth_handler: AuthPKCE = AuthPKCE(Spotify.CLIENT_ID, self.cache)

    @property
    def cache(self) -> Cache:
        return self._cache

    @property
    def auth_handler(self) -> AuthPKCE:
        return self._auth_handler

    def get_access_token(self) -> None:
        self._access_token: str = self.auth_handler.get_access_token()

    @staticmethod
    def _url(suffix: str, query: JSONObject | None = None) -> str:
        url: str = f"{Spotify.BASE_URL}{suffix}"
        if query is None:
            return url
        return f"{url}?{urlencode(query)}"

    def _request(
        self,
        method: str,
        url: str,
        body: bytes | str | None = None,
        attempts: int = 0,
    ) -> bytes:
        if attempts == Spotify.MAX_ATTEMPTS:
            raise Exception(f"Reached max attempts for {method} {url}")
        if not hasattr(self, "_access_token"):
            self.get_access_token()
        logging.debug(f"Sending {method} request to {url} with {body}")
        request: Request = Request(
            method=method,
            url=url,
            data=body.encode() if isinstance(body, str) else body,
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        response: HTTPResponse = urlopen(request)
        if response.status == 403:
            logging.debug("403 response from {url}, refreshing access token")
            self.get_access_token()
            return self._request(method, url, attempts=attempts + 1)
        return response.read()

    def _player_request(
        self,
        method: str,
        url: str,
        body: bytes | str | None = None,
        attempts: int = 0,
    ) -> bytes:
        try:
            return self._request(method, url, body, attempts)
        except HTTPError:
            raise NotImplementedError("Device not found: Please specify device")

    def get_top(
        self,
        item_type: str,
        term: str = "medium_term",
        limit: int = 20,
        offset: int = 0,
    ) -> Iterator[tuple[int, JSONObject]]:
        params: dict[str, str | int] = {
            "time_range": term,
            "limit": limit,
            "offset": offset,
        }
        url: str = Spotify._url(f"me/top/{item_type}", params)
        response: bytes = self._request("GET", url)
        tracks: JSONObject = json.loads(response)
        rank: int = offset + 1
        for n, item in enumerate(tracks["items"]):
            yield rank + n, item

    def get_saved_tracks(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> Iterator[JSONObject]:
        params: dict[str, int] = {"limit": limit, "offset": offset}
        url: str = Spotify._url(f"me/tracks", params)
        response: bytes = self._request("GET", url)
        yield from json.loads(response)["items"]

    def get_devices(self) -> Iterator[JSONObject]:
        url: str = Spotify._url(f"me/player/devices")
        response: bytes = self._request("GET", url)
        yield from json.loads(response)["devices"]

    def previous(self, device_id: str | None = None) -> bytes:
        params: dict[str, str] = {}
        if device_id is not None:
            params["device_id"] = device_id
        url: str = Spotify._url("me/player/next", params)
        return self._player_request("POST", url)

    def next(self, device_id: str | None = None) -> bytes:
        params: dict[str, str] = {}
        if device_id is not None:
            params["device_id"] = device_id
        url: str = Spotify._url("me/player/next", params)
        return self._player_request("POST", url)
