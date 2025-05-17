from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
import logging

from ._base import Command
from parsers import number, offset
from spotify import Spotify
from type_definitions import JSONObject


class GetSavedTracks(Command):
    DESCRIPTION: str = "Get your saved tracks"

    DEFAULT_LIMIT: int = 20
    DEFAULT_OFFSET: int = 0
    MAX_PER_REQUEST: int = 50

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [
            number(GetSavedTracks.DEFAULT_LIMIT, "Number of tracks to pull"),
            offset(
                default=GetSavedTracks.DEFAULT_OFFSET,
                help_string="Position to start pulling from",
            ),
        ]

    def __init__(self, args: Namespace) -> None:
        self._args: Namespace = args
        for item in self._results():
            added_at: str = item["added_at"]
            track: JSONObject = item["track"]
            artists: list[str] = [artist["name"] for artist in track["artists"]]
            name: str = track["name"]
            print(f"{name:<50}{', '.join(artists):<50}{added_at}")

    def _results(self) -> Iterator[JSONObject]:
        client: Spotify = Spotify()
        for n in range(
            self._args.offset,
            self._args.number + self._args.offset,
            GetSavedTracks.MAX_PER_REQUEST,
        ):
            remaining: int = self._args.number + self._args.offset - n
            limit: int = min(remaining, GetSavedTracks.MAX_PER_REQUEST)
            logging.debug(f"Requesting {n}-{n + limit}")
            yield from client.get_saved_tracks(limit, n)
