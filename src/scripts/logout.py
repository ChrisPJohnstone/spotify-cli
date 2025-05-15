from argparse import ArgumentParser, Namespace

from ._base import Command
from src.spotify import Spotify


class LogOut(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return []

    def __init__(self, _: Namespace) -> None:
        Spotify().clear_cache()
