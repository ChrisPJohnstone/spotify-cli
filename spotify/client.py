from base64 import urlsafe_b64encode
from collections.abc import Iterator
from hashlib import sha256
from random import choice
from string import ascii_letters, digits
from urllib.parse import urlencode
from urllib3 import BaseHTTPResponse, request
import json
import logging
import webbrowser

from .auth_server import AuthServer
from type_definitions import JSONObject


class Client:
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

    def __init__(self) -> None:
        self.get_access_token()

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
            "client_id": Client.CLIENT_ID,
            "redirect_uri": Client.REDIRECT_URI,
            "code_challenge": self._code_challenge,
            "code_challenge_method": 'S256',
            "response_type": "code",
            "scope": " ".join(Client.SCOPE),
        }
        output: str = f"{Client.AUTH_URL}?{urlencode(payload)}"
        logging.debug(f"Auth url: {output}")
        return output

    def get_auth_code(self) -> None:
        # TODO: Add some kinda caching for this so it doesn't need to request on every run
        server: AuthServer = AuthServer(Client.REDIRECT_URI)
        webbrowser.open(self.auth_url())
        print("Go to your browser to authenticate")
        server.handle_request()
        self._auth_code: str = server._auth_code

    def get_access_token(self) -> None:
        if not hasattr(self, "_auth_code"):
            self.get_auth_code()
        payload: dict[str, str] = {
            "client_id": Client.CLIENT_ID,
            "redirect_uri": Client.REDIRECT_URI,
            "code": self._auth_code,
            "code_verifier": self._code_verifier,
            "grant_type": "authorization_code",
        }
        response: BaseHTTPResponse = request(
            method="POST",
            url=Client.TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            body=urlencode(payload),
        )
        response_data: JSONObject = json.loads(response.data)
        if "access_token" not in response_data:
            raise Exception(f"Authentication failed: {response_data}")
        self._access_token: str = response_data["access_token"]

    @property
    def access_token(self) -> str:
        return self._access_token

    def _request(self, method: str, url: str, attempts: int = 0) -> JSONObject:
        if attempts == Client.MAX_ATTEMPTS:
            raise Exception(f"Reached max attempts for {method} {url}")
        response: BaseHTTPResponse = request(
            method=method,
            url=url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status == 403:
            self.get_access_token()
            return self._request(method, url, attempts + 1)
        return json.loads(response.data)

    def get_top_tracks(self) -> Iterator[JSONObject]:
        url: str = f"{Client.BASE_URL}me/top/tracks"
        response: JSONObject = self._request("GET", url)
        for item in response["items"]:
            yield item
