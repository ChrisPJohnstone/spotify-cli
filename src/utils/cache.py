from pathlib import Path
import json
import logging


class Cache:
    CACHE_DIR: Path = Path.home() / ".cache" / "spotify-cli"
    CACHE_FILENAME: str = "cache.json"

    def __init__(self) -> None:
        Cache.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return Cache.CACHE_DIR / Cache.CACHE_FILENAME

    def clear(self) -> None:
        if not self.path.is_file():
            return
        logging.debug(f"Deleting {self.path}")
        self.path.unlink()

    def read(self) -> dict[str, str]:
        if not self.path.is_file():
            return {}
        logging.debug(f"Reading {self.path}")
        cache: str = self.path.read_text()
        if len(cache) == 0:
            return {}
        return json.loads(cache)

    def write(self, content: dict[str, str]) -> None:
        if not self.path.is_file():
            self.path.touch(exist_ok=True)
        logging.debug(f"Updating {self.path} with {content}")
        new: dict[str, str] = {**self.read(), **content}
        self.path.write_text(json.dumps(new))
