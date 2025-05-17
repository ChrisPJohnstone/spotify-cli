from argparse import ArgumentParser, Namespace

from ._base import Command
from src.spotify import Spotify


class GetDevices(Command):
    DESCRIPTION: str = "Get avaiable devices"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return []

    def __init__(self, _: Namespace) -> None:
        client: Spotify = Spotify()
        header: bool = True
        for device in client.get_devices():
            if header:
                print(f"{'Name':<30}{'is_active':<15}{'is_private_session'}")
                header: bool = False
            name: str = device["name"]
            is_active: bool = device["is_active"]
            is_private_session: bool = device["is_private_session"]
            print(f"{name:<30}{is_active:<15}{int(is_private_session)}")
