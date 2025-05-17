from argparse import ArgumentParser, Namespace

from ._player import Player
from src.parsers import device
from src.spotify import Spotify


class PlayerNext(Player):
    DESCRIPTION: str = "Move to the next song in queue"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [device()]

    def __init__(self, args: Namespace) -> None:
        self._args: Namespace = args
        self._client: Spotify = Spotify()
        self._client.next(self.get_device())
