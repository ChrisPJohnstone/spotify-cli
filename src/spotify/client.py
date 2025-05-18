from base64 import urlsafe_b64encode
from collections.abc import Iterator
from hashlib import sha256
from http.client import HTTPResponse
from random import choice
from string import ascii_letters, digits
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import logging
import webbrowser

from .auth_server import AuthServer
from type_definitions import JSONObject
from utils import Cache


class Spotify:
    CLIENT_ID: str = "b37fc55dfdd8409db2411464ba60ef5e"
    REDIRECT_URI: str = "http://127.0.0.1:8080"
    AUTH_URL: str = "https://accounts.spotify.com/authorize"
    TOKEN_URL: str = "https://accounts.spotify.com/api/token"
    BASE_URL: str = "https://api.spotify.com/v1/"
    MAX_ATTEMPTS: int = 3
    SCOPE: list[str] = [
        # https://developer.spotify.com/documentation/web-api/concepts/scopes
        "user-library-read",
        "user-modify-playback-state",
        "user-read-playback-state",
        "user-top-read",
    ]

    def __init__(self) -> None:
        self._cache: Cache = Cache()

    @property
    def cache(self) -> Cache:
        return self._cache

    def generate_code_verifier(self, length: int = 128) -> None:
        letters: str = ascii_letters + digits
        constructor: list[str] = [choice(letters) for _ in range(length)]
        self._code_verifier: str = "".join(constructor)
        logging.debug(f"Code verifier generated {self._code_verifier}")

    def generate_code_challenge(self) -> None:
        if not hasattr(self, "_code_verifier"):
            self.generate_code_verifier()
        digest: bytes = sha256(self._code_verifier.encode("UTF-8")).digest()
        encoded: str = urlsafe_b64encode(digest).decode()
        self._code_challenge: str = encoded.replace("=", "")
        logging.debug(f"Code challenge generated: {self._code_challenge}")

    def auth_url(self) -> str:
        if not hasattr(self, "_code_challenge"):
            self.generate_code_challenge()
        payload: dict[str, str] = {
            "client_id": Spotify.CLIENT_ID,
            "redirect_uri": Spotify.REDIRECT_URI,
            "code_challenge": self._code_challenge,
            "code_challenge_method": "S256",
            "response_type": "code",
            "scope": " ".join(Spotify.SCOPE),
        }
        output: str = f"{Spotify.AUTH_URL}?{urlencode(payload)}"
        logging.debug(f"Auth url: {output}")
        return output

    def get_auth_code(self) -> None:
        """
        1. Starts server which is waiting for an auth code to be sent to it
        2. Opens spotify authentication in a browser
        3. Once you authenticate in browser it'll send auth code to server
        """
        server: AuthServer = AuthServer(Spotify.REDIRECT_URI)
        webbrowser.open(self.auth_url())
        print("Go to your browser to authenticate")
        server.handle_request()
        self._auth_code: str = server._auth_code

    def _get_access_token(self, payload: dict[str, str]) -> None:
        logging.debug(f"Requesting new access token with payload {payload}")
        request: Request = Request(
            method="POST",
            url=Spotify.TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode(payload).encode(),
        )
        response: HTTPResponse = urlopen(request)
        response_data: JSONObject = json.loads(response.read())
        if "access_token" not in response_data:
            raise Exception(f"Authentication failed: {response_data}")
        self.cache.write({"refresh_token": response_data["refresh_token"]})
        self._access_token: str = response_data["access_token"]

    def get_access_token(self) -> None:
        cache: dict[str, str] = self.cache.read()
        if "refresh_token" in cache:
            payload: dict[str, str] = {
                "client_id": Spotify.CLIENT_ID,
                "grant_type": "refresh_token",
                "refresh_token": cache["refresh_token"],
            }
        else:
            if not hasattr(self, "_auth_code"):
                self.get_auth_code()
            payload: dict[str, str] = {
                "client_id": Spotify.CLIENT_ID,
                "redirect_uri": Spotify.REDIRECT_URI,
                "code": self._auth_code,
                "code_verifier": self._code_verifier,
                "grant_type": "authorization_code",
            }
        self._get_access_token(payload)

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
