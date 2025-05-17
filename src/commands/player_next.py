from argparse import ArgumentParser, Namespace

from ._base import Command
from src.spotify import Spotify


class PlayerNext(Command):
    DESCRIPTION: str = "Move to the next song in queue"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return []

    def __init__(self, _: Namespace) -> None:
        Spotify().next()
