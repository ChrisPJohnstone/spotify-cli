#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
import logging

from src.spotify import Spotify


def main() -> None:
    client: Spotify = Spotify()
    for track in client.get_top_tracks():
        artists: list[str] = [artist["name"] for artist in track["artists"]]
        print("".join(artists), track["name"])


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser(
        prog="Spotify CLI Interface (very unfinished)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
