from argparse import Namespace

from ._base import Command
from src.spotify import Spotify


class Player(Command):
    @property
    def args(self) -> Namespace:  # pragma: no cover
        if not hasattr(self, "_args"):
            raise ValueError("_args must be set in __init__")
        return self._args  # type: ignore

    @property
    def client(self) -> Spotify:  # pragma: no cover
        if not hasattr(self, "_client"):
            raise ValueError("_client must be set in __init__")
        return self._client  # type: ignore

    def get_device(self) -> str | None:
        if len(self.args.device) == 0:
            return None
        devices: dict[str, str] = {
            device["name"]: device["id"] for device in self.client.get_devices()
        }
        device: str = " ".join(self.args.device)
        if device in devices:
            return devices[device]
        raise ValueError(f"{device} not found in {devices}")
