from argparse import Namespace, RawTextHelpFormatter
from logging import DEBUG
from unittest.mock import _Call, ANY, MagicMock, call, patch

from src.__main__ import main
from test_utils import TestSet, parametrize

FILEPATH: str = "src.__main__"


main_tests: TestSet = {
    "single": {
        "shared": ["verbose"],
        "args": Namespace(command="test", number=20),
        "commands": ["test"],
        "expected_logging_calls": [],
    },
    "verbose": {
        "shared": ["verbose"],
        "args": Namespace(command="test", verbose=True, number=20),
        "commands": ["test"],
        "expected_logging_calls": [call.basicConfig(level=DEBUG)],
    },
    "multi": {
        "shared": ["verbose"],
        "args": Namespace(command="bar", number=20),
        "commands": ["foo", "bar"],
        "expected_logging_calls": [],
    },
}


@patch(f"{FILEPATH}.basicConfig")
@patch(f"{FILEPATH}.ArgumentParser")
@parametrize(main_tests)
def test_main(
    mock_argument_parser: MagicMock,
    mock_logging_config: MagicMock,
    shared: list[str],
    args: Namespace,
    commands: list[str],
    expected_logging_calls: list[_Call],
) -> None:
    mock_parse_args: MagicMock = mock_argument_parser.return_value.parse_args
    mock_parse_args.return_value = args
    with patch(
        target=f"{FILEPATH}.SHARED",
        new=[MagicMock(parser) for parser in shared],
    ):
        with patch(
            target=f"{FILEPATH}.COMMANDS",
            new={command: MagicMock() for command in commands},
        ) as mock_commands:
            main()
    mock_logging_config.assert_has_calls(expected_logging_calls)
    mock_argument_parser.assert_called_once_with(
        prog="spotify",
        description="Spotify Command Line Interface",
        formatter_class=RawTextHelpFormatter,
        parents=[*[ANY for _ in range(len(shared))]],
        usage="%(prog)s [options] <command> [parameters]",
    )
    mock_parser: MagicMock = mock_argument_parser.return_value
    mock_add_subparsers: MagicMock = mock_parser.add_subparsers
    mock_add_subparsers.assert_called_once_with(
        title="commands",
        dest="command",
        metavar="\n  ".join(commands),
        required=True,
    )
    mock_subparsers: MagicMock = mock_add_subparsers.return_value
    add_parser_calls: list[_Call] = [
        call(
            name=name,
            prog=f"spotify {name}",
            formatter_class=RawTextHelpFormatter,
            parents=[*[ANY for _ in range(len(shared))]],
        )
        for name in mock_commands.keys()
    ]
    mock_subparsers.add_parser.assert_has_calls(add_parser_calls)
    for mock_command in mock_commands.values():
        mock_command.parent_parsers.assert_called_once()
    mock_commands[args.command].assert_called_once_with(args)
