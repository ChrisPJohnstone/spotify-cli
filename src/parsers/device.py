from argparse import ArgumentParser


def device() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        dest="device",
        nargs="*",
        type=str,
        default=None,
        help=(
            "Device name to play on. If not specified defaults to user's "
            "active device. If no device is active you will be presented with "
            "an error."
        ),
    )
    return parser
