from argparse import ArgumentParser


def term(default: int, help_string: str) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--term",
        type=str,
        choices=["short_term", "medium_term", "long_term"],
        default=default,
        help=f"{help_string} (Default: {default})",
    )
    return parser
