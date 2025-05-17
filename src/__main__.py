from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)
from logging import DEBUG, basicConfig

from src.commands import (
    Command,
    GetSavedTracks,
    GetTopArtists,
    GetTopTracks,
    LogOut,
    PlayerNext,
    PlayerPrevious,
)
from src.parsers import SHARED

COMMANDS: dict[str, type[Command]] = {
    "logout": LogOut,
    "next": PlayerNext,
    "previous": PlayerPrevious,
    "saved-tracks": GetSavedTracks,
    "top-artists": GetTopArtists,
    "top-tracks": GetTopTracks,
}


def _epilog() -> str:
    max_command_len: int = max(map(len, COMMANDS.keys())) + 4
    join_string: str = "\n  "
    commands: list[str] = [
        f"{name:<{max_command_len}}{command.DESCRIPTION}"
        for name, command in COMMANDS.items()
    ]
    return f"commands:{join_string}{join_string.join(commands)}"


def main() -> None:
    parser: ArgumentParser = ArgumentParser(
        prog="spotify",
        description="Spotify Command Line Interface",
        formatter_class=RawTextHelpFormatter,
        parents=[parser(True) for parser in SHARED],
        usage="%(prog)s [options] <command> [parameters]",
        epilog=_epilog(),
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        dest="command",
        metavar="command",
        required=True,
    )
    shared: list[ArgumentParser] = [parser() for parser in SHARED]
    for name, command in COMMANDS.items():
        subparsers.add_parser(
            name=name,
            description=command.DESCRIPTION,
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
