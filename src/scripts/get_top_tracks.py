from argparse import ArgumentParser, Namespace

from src.parsers import number, offset, term
from src.spotify import Spotify
from .base import Command


class GetTopTracks(Command):
    DEFAULT_LIMIT: int = 20
    DEFAULT_OFFSET: int = 0
    DEFAULT_TERM: str = "medium_term"

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [
            number(GetTopTracks.DEFAULT_LIMIT, "Number of tracks to pull"),
            offset(GetTopTracks.DEFAULT_OFFSET, "Rank to start pulling from"),
            term(
                default=GetTopTracks.DEFAULT_TERM,
                help_string="Over what time frame affinity is computed",
            ),
        ]

    def __init__(self, args: Namespace) -> None:
        client: Spotify = Spotify()
        for track in client.get_top_tracks(args.term, args.number, args.offset):
            artists: list[str] = [artist["name"] for artist in track["artists"]]
            print("".join(artists), track["name"])
