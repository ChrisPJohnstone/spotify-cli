from argparse import _SubParsersAction, ArgumentParser, Namespace
import logging

from .base import Command
from .get_top_tracks import GetTopTracks
from src.parsers import SHARED

COMMANDS: dict[str, type[Command]] = {
    "top-tracks": GetTopTracks,
}


def main() -> None:
    shared: list[ArgumentParser] = [parser() for parser in SHARED]
    parser: ArgumentParser = ArgumentParser(
        description="Spotify CLI Interface (very unfinished)",
        parents=shared,
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        title="command",
        dest="command",
        metavar="<command>",
        required=True,
    )
    for name, command in COMMANDS.items():
        subparsers.add_parser(
            name=name,
            parents=[*shared, *command.parent_parsers()],
        )
    args: Namespace = parser.parse_args()
    if getattr(args, "verbose", False):
        logging.basicConfig(level=logging.DEBUG)
    COMMANDS[args.command](args)
