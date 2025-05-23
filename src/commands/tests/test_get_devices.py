from argparse import Namespace
from unittest.mock import _Call, MagicMock, call, patch

from commands import GetDevices
from type_definitions import JSONObject
from test_utils import TestSet, parametrize

FILEPATH: str = "commands.get_devices"


def test_parent_parsers() -> None:
    assert GetDevices.parent_parsers() == []


init_tests: TestSet = {
    "none": {"devices": [], "expected_print_calls": []},
    "single": {
        "devices": [
            {
                "id": "u-u-id",
                "name": "Living Room Speaker",
                "is_active": False,
                "is_private_session": False,
            },
        ],
        "expected_print_calls": [
            call(
                f"{'name':<30}{'is_active':<15}{'is_private_session':<20}device_id"
            ),
            call(f"{'Living Room Speaker':<30}{'0':<15}{'0':<20}u-u-id"),
        ],
    },
    "multi": {
        "devices": [
            {
                "id": "foo",
                "name": "Living Room Speaker",
                "is_active": False,
                "is_private_session": False,
            },
            {
                "id": "bar",
                "name": "Kitchen Speaker",
                "is_active": True,
                "is_private_session": True,
            },
        ],
        "expected_print_calls": [
            call(
                f"{'name':<30}{'is_active':<15}{'is_private_session':<20}device_id"
            ),
            call(f"{'Living Room Speaker':<30}{'0':<15}{'0':<20}foo"),
            call(f"{'Kitchen Speaker':<30}{'1':<15}{'1':<20}bar"),
        ],
    },
}


@patch("builtins.print")
@patch(f"{FILEPATH}.Spotify")
@parametrize(init_tests)
def test_init(
    mock_spotify: MagicMock,
    mock_print: MagicMock,
    devices: list[JSONObject],
    expected_print_calls: list[_Call],
) -> None:
    mock_client: MagicMock = mock_spotify.return_value
    mock_get_devices: MagicMock = mock_client.get_devices
    mock_get_devices.return_value = devices
    GetDevices(Namespace())
    mock_print.assert_has_calls(expected_print_calls)
