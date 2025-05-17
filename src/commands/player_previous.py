from argparse import ArgumentParser, Namespace

from ._player import Player
from parsers import device
from spotify import Spotify


class PlayerPrevious(Player):
    DESCRIPTION: str = "Move to the previous song in queue"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [device()]

    def __init__(self, args: Namespace) -> None:
        self._args: Namespace = args
        self._client: Spotify = Spotify()
        self._client.previous(self.get_device())
