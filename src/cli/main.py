from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)
from logging import DEBUG, basicConfig

from ._base import Command
from .get_saved_tracks import GetSavedTracks
from .get_top_artists import GetTopArtists
from .get_top_tracks import GetTopTracks
from .logout import LogOut
from .player_next import PlayerNext
from .player_previous import PlayerPrevious
from src.parsers import SHARED

COMMANDS: dict[str, type[Command]] = {
    "logout": LogOut,
    "next": PlayerNext,
    "previous": PlayerPrevious,
    "saved-tracks": GetSavedTracks,
    "top-artists": GetTopArtists,
    "top-tracks": GetTopTracks,
}


def main() -> None:
    parser: ArgumentParser = ArgumentParser(
        description="Spotify CLI Interface (very unfinished)",
        formatter_class=RawTextHelpFormatter,
        parents=[parser(True) for parser in SHARED],
        usage="%(prog)s [options] <command> [parameters]",
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        title="commands",
        dest="command",
        metavar=f"{'\n  '.join(COMMANDS.keys())}",
        required=True,
    )
    shared: list[ArgumentParser] = [parser() for parser in SHARED]
    for name, command in COMMANDS.items():
        subparsers.add_parser(
            name=name,
            formatter_class=RawTextHelpFormatter,
            parents=[*shared, *command.parent_parsers()],
        )
    args: Namespace = parser.parse_args()
    if getattr(args, "verbose", False):
        basicConfig(level=DEBUG)
    COMMANDS[args.command](args)
