from argparse import ArgumentParser


def number(default: int, help_string: str) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-n",
        "--number",
        default=default,
        help=f"{help_string} (Default: {default})",
    )
    return parser
