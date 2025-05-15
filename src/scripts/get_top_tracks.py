#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace

from src.parsers import number
from src.spotify import Spotify
from .base import Command


class GetTopTracks(Command):
    DEFAULT_N: int = 20

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [
            number(GetTopTracks.DEFAULT_N, "Number of tracks to pull"),
        ]

    def __init__(self, args: Namespace) -> None:
        # TODO: Add support for number
        client: Spotify = Spotify()
        for track in client.get_top_tracks():
            artists: list[str] = [artist["name"] for artist in track["artists"]]
            print("".join(artists), track["name"])
