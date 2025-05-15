from base64 import urlsafe_b64encode
from collections.abc import Iterator
from hashlib import sha256
from pathlib import Path
from random import choice
from string import ascii_letters, digits
from urllib.parse import urlencode
from urllib3 import BaseHTTPResponse, request
import json
import logging
import webbrowser

from .auth_server import AuthServer
from src.type_definitions import JSONObject


class Spotify:
    CACHE_DIR: Path = Path.home() / ".cache" / "spotify-cli"
    CLIENT_ID: str = "b37fc55dfdd8409db2411464ba60ef5e"
    REDIRECT_URI: str = "http://127.0.0.1:8080"
    AUTH_URL: str = "https://accounts.spotify.com/authorize"
    TOKEN_URL: str = "https://accounts.spotify.com/api/token"
    BASE_URL: str = "https://api.spotify.com/v1/"
    MAX_ATTEMPTS: int = 3
    SCOPE: list[str] = [
        # https://developer.spotify.com/documentation/web-api/concepts/scopes
        "user-top-read",
    ]

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
        server: AuthServer = AuthServer(Spotify.REDIRECT_URI)
        webbrowser.open(self.auth_url())
        print("Go to your browser to authenticate")
        server.handle_request()
        self._auth_code: str = server._auth_code

    @property
    def cache_path(self) -> Path:
        Spotify.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        return Spotify.CACHE_DIR / "auth.txt"

    def read_cache(self) -> dict[str, str]:
        if not self.cache_path.is_file():
            return {}
        cache: str = self.cache_path.read_text()
        if len(cache) == 0:
            return {}
        return json.loads(cache)

    def write_cache(self, content: dict[str, str]) -> None:
        if not self.cache_path.is_file():
            self.cache_path.touch(exist_ok=True)
        new_cache: dict[str, str] = {
            **self.read_cache(),
            **content,
        }
        self.cache_path.write_text(json.dumps(new_cache))

    def _get_access_token(self, payload: dict[str, str]) -> None:
        response: BaseHTTPResponse = request(
            method="POST",
            url=Spotify.TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            body=urlencode(payload),
        )
        response_data: JSONObject = json.loads(response.data)
        if "access_token" not in response_data:
            raise Exception(f"Authentication failed: {response_data}")
        self.write_cache({"refresh_token": response_data["refresh_token"]})
        self._access_token: str = response_data["access_token"]

    def get_access_token(self) -> None:
        cache: dict[str, str] = self.read_cache()
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
        response: BaseHTTPResponse = request(
            method=method,
            url=url,
            body=body,
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        if response.status == 403:
            logging.debug("403 response from {url}, refreshing access token")
            self.get_access_token()
            return self._request(method, url, attempts=attempts + 1)
        return response.data

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
        url: str = f"{Spotify.BASE_URL}me/top/{item_type}?{urlencode(params)}"
        response: bytes = self._request("GET", url)
        tracks: JSONObject = json.loads(response)
        rank: int = offset + 1
        for n, item in enumerate(tracks["items"]):
            yield rank + n, item
