from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)
from logging import DEBUG, basicConfig

from .commands._base import Command
from .commands.get_saved_tracks import GetSavedTracks
from .commands.get_top_artists import GetTopArtists
from .commands.get_top_tracks import GetTopTracks
from .commands.logout import LogOut
from .commands.player_next import PlayerNext
from .commands.player_previous import PlayerPrevious
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
        prog="spotify",
        description="Spotify CLI Interface",
        formatter_class=RawTextHelpFormatter,
        parents=[parser(True) for parser in SHARED],
        usage="%(prog)s [options] <command> [parameters]",
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="\n  ".join(COMMANDS.keys()),
        # TODO: Add help strings to this
        # TODO: When you run app without args these all list as required
        required=True,
    )
    shared: list[ArgumentParser] = [parser() for parser in SHARED]
    for name, command in COMMANDS.items():
        subparsers.add_parser(
            name=name,
            prog=f"spotify {name}",
            formatter_class=RawTextHelpFormatter,
            parents=[*shared, *command.parent_parsers()],
        )
    args: Namespace = parser.parse_args()
    if getattr(args, "verbose", False):
        basicConfig(level=DEBUG)
    COMMANDS[args.command](args)


if __name__ == "__main__":
    main()
