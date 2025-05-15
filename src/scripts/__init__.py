from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)
import logging

from ._base import Command
from .get_top_artists import GetTopArtists
from .get_top_tracks import GetTopTracks
from .logout import LogOut
from src.parsers import SHARED

COMMANDS: dict[str, type[Command]] = {
    "logout": LogOut,
    "top-artists": GetTopArtists,
    "top-tracks": GetTopTracks,
}


def main() -> None:
    shared: list[ArgumentParser] = [parser() for parser in SHARED]
    parser: ArgumentParser = ArgumentParser(
        description="Spotify CLI Interface (very unfinished)",
        formatter_class=RawTextHelpFormatter,
        parents=shared,
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        title="command",
        dest="command",
        metavar="<command>",
        help=f"One of:\n- {'\n- '.join(COMMANDS.keys())}",
        required=True,
    )
    for name, command in COMMANDS.items():
        subparsers.add_parser(
            name=name,
            formatter_class=RawTextHelpFormatter,
            parents=[*shared, *command.parent_parsers()],
        )
    args: Namespace = parser.parse_args()
    if getattr(args, "verbose", False):
        logging.basicConfig(level=logging.DEBUG)
    COMMANDS[args.command](args)
