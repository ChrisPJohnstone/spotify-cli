from abc import ABC, abstractmethod

from utils import Cache


class SpotifyAuth(ABC):
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

    @abstractmethod
    def get_access_token(self) -> str:  # pragma: no cover
        pass
