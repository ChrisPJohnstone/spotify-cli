from argparse import ArgumentParser, SUPPRESS


def verbose() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-v",
        "--verbose",
        default=SUPPRESS,
        action="store_true",
        help="Enable verbose logging",
    )
    return parser
