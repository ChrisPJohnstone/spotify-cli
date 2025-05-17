from argparse import ArgumentParser


def offset(default: int, help_string: str) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--offset",
        metavar="offset",
        type=int,
        default=default,
        help=f"{help_string} (Default: {default})",
    )
    return parser
