from argparse import ArgumentParser, Namespace

from ._base import Command
from src.spotify import Spotify


class PlayerPrevious(Command):
    DESCRIPTION: str = "Move to the previous song in queue"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return []

    def __init__(self, _: Namespace) -> None:
        Spotify().previous()
