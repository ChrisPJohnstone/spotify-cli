from argparse import ArgumentParser, SUPPRESS


def verbose(is_top: bool = False) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-v",
        "--verbose",
        default=False if is_top else SUPPRESS,
        action="store_true",
        help="Enable verbose logging",
    )
    return parser
