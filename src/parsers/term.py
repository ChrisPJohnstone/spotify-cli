from argparse import ArgumentParser


def term(default: int, help_string: str) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--term",
        type=str,
        choices=["short_term", "medium_term", "long_term"],
        default=default,
        help=(
            f"{help_string} (Default: {default})\n"
            "- short_term   4 weeks\n"
            "- medium_term  6 months\n"
            "- long_term    1 year\n"
        ),
    )
    return parser
