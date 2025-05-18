from argparse import ArgumentParser, Namespace

from ._base import Command
from spotify import Spotify


class LogOut(Command):
    DESCRIPTION: str = "Clear cache so log in is required for future requests"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return []

    def __init__(self, _: Namespace) -> None:
        Spotify().cache.clear()
