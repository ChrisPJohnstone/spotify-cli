from argparse import ArgumentParser, Namespace

from ._base import Command
from src.spotify import Spotify


class GetDevices(Command):
    DESCRIPTION: str = "Get avaiable devices"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return []

    @staticmethod
    def _print_device(
        name: str,
        is_active: str,
        is_private_session: str,
        device_id: str,
    ) -> None:
        output: str = ""
        output += f"{name:<30}"
        output += f"{is_active:<15}"
        output += f"{is_private_session:<20}"
        output += f"{device_id}"
        print(output)

    def __init__(self, _: Namespace) -> None:
        client: Spotify = Spotify()
        header: bool = True
        for device in client.get_devices():
            if header:
                GetDevices._print_device(
                    name="name",
                    is_active="is_active",
                    is_private_session="is_private_session",
                    device_id="device_id",
                )
                header: bool = False
            GetDevices._print_device(
                name=device["name"],
                is_active=device["is_active"],
                is_private_session=device["is_private_session"],
                device_id=device["id"],
            )
