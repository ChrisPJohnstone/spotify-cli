from argparse import Namespace
from unittest.mock import MagicMock, PropertyMock, patch

from pytest import raises

from src.commands._player import Player
from test_utils import TestSet, parametrize


get_device_tests: TestSet = {
    "none": {
        "args": Namespace(device=[]),
        "devices": [{"id": "test", "name": "Speaker"}],
        "expected": None,
    },
    "Speaker": {
        "args": Namespace(device=["Speaker"]),
        "devices": [{"id": "test", "name": "Speaker"}],
        "expected": "test",
    },
}


@patch.object(Player, "client", new_callable=PropertyMock)
@patch.object(Player, "args", new_callable=PropertyMock)
@patch.object(Player, "__init__", MagicMock(return_value=None))
@patch.object(Player, "__abstractmethods__", set())
@parametrize(get_device_tests)
def test_get_device(
    mock_args: PropertyMock,
    mock_client: PropertyMock,
    args: Namespace,
    devices: list[dict[str, str]],
    expected: str | None,
) -> None:
    mock_args.return_value = args
    mock_client.return_value.get_devices.return_value = devices
    player: Player = Player()  # type: ignore
    assert player.get_device() == expected


get_device_not_found_tests: TestSet = {
    "foo": {
        "args": Namespace(device=["foo"]),
        "devices": [{"id": "test", "name": "Speaker"}],
        "expected": "foo not found in {'Speaker': 'test'}",
    },
    "bar": {
        "args": Namespace(device=["bar"]),
        "devices": [{"id": "test", "name": "Speaker"}],
        "expected": "bar not found in {'Speaker': 'test'}",
    },
}


@patch.object(Player, "client", new_callable=PropertyMock)
@patch.object(Player, "args", new_callable=PropertyMock)
@patch.object(Player, "__init__", MagicMock(return_value=None))
@patch.object(Player, "__abstractmethods__", set())
@parametrize(get_device_not_found_tests)
def test_get_device_not_found(
    mock_args: PropertyMock,
    mock_client: PropertyMock,
    args: Namespace,
    devices: list[dict[str, str]],
    expected: str | None,
) -> None:
    mock_args.return_value = args
    mock_client.return_value.get_devices.return_value = devices
    player: Player = Player()  # type: ignore
    with raises(ValueError, match=expected):
        player.get_device()
