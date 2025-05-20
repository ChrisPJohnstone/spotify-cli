from base64 import urlsafe_b64encode
from hashlib import sha256
from http.client import HTTPResponse
from random import choice
from string import ascii_letters, digits
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import logging
import webbrowser

from type_definitions import JSONObject
from utils import AuthServer, Cache


class AuthPKCE:
    CLIENT_ID: str = "b37fc55dfdd8409db2411464ba60ef5e"
    REDIRECT_URI: str = "http://127.0.0.1:8080"
    AUTH_URL: str = "https://accounts.spotify.com/authorize"
    TOKEN_URL: str = "https://accounts.spotify.com/api/token"
    SCOPE: list[str] = [
        # https://developer.spotify.com/documentation/web-api/concepts/scopes
        "user-library-read",
        "user-modify-playback-state",
        "user-read-playback-state",
        "user-top-read",
    ]

    def __init__(self, cache: Cache) -> None:
        self._cache: Cache = cache

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
            "client_id": AuthPKCE.CLIENT_ID,
            "redirect_uri": AuthPKCE.REDIRECT_URI,
            "code_challenge": self._code_challenge,
            "code_challenge_method": "S256",
            "response_type": "code",
            "scope": " ".join(AuthPKCE.SCOPE),
        }
        output: str = f"{AuthPKCE.AUTH_URL}?{urlencode(payload)}"
        logging.debug(f"Auth url: {output}")
        return output

    def get_auth_code(self) -> None:
        """
        1. Starts server which is waiting for an auth code to be sent to it
        2. Opens spotify authentication in a browser
        3. Once you authenticate in browser it'll send auth code to server
        """
        server: AuthServer = AuthServer(AuthPKCE.REDIRECT_URI)
        webbrowser.open(self.auth_url())
        print("Go to your browser to authenticate")
        server.handle_request()
        self._auth_code: str = server._auth_code

    def _get_access_token(self, payload: dict[str, str]) -> str:
        logging.debug(f"Requesting new access token with payload {payload}")
        request: Request = Request(
            method="POST",
            url=AuthPKCE.TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode(payload).encode(),
        )
        response: HTTPResponse = urlopen(request)
        response_data: JSONObject = json.loads(response.read())
        if "access_token" not in response_data:
            raise Exception(f"Authentication failed: {response_data}")
        self.cache.write({"refresh_token": response_data["refresh_token"]})
        return response_data["access_token"]

    def get_access_token(self) -> str:
        cache: dict[str, str] = self.cache.read()
        if "refresh_token" in cache:
            payload: dict[str, str] = {
                "client_id": AuthPKCE.CLIENT_ID,
                "grant_type": "refresh_token",
                "refresh_token": cache["refresh_token"],
            }
        else:
            if not hasattr(self, "_auth_code"):
                self.get_auth_code()
            payload: dict[str, str] = {
                "client_id": AuthPKCE.CLIENT_ID,
                "redirect_uri": AuthPKCE.REDIRECT_URI,
                "code": self._auth_code,
                "code_verifier": self._code_verifier,
                "grant_type": "authorization_code",
            }
        return self._get_access_token(payload)
