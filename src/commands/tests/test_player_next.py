from argparse import Namespace
from unittest.mock import MagicMock, call, patch

from commands import PlayerNext
from test_utils import TestSet, parametrize

FILEPATH: str = "commands.player_next"


@patch(f"{FILEPATH}.device")
def test_parent_parsers(mock_device: MagicMock) -> None:
    assert PlayerNext.parent_parsers() == [mock_device.return_value]
    mock_device.assert_called_once()


init_tests: TestSet = {
    "none": {"device": None},
    "speaker": {"device": "Speaker"},
}


@patch.object(PlayerNext, "get_device")
@patch(f"{FILEPATH}.Spotify")
@parametrize(init_tests)
def test_init(
    mock_spotify: MagicMock,
    mock_get_device: MagicMock,
    device: str | None,
) -> None:
    mock_get_device.return_value = device
    PlayerNext(Namespace())
    mock_spotify.assert_has_calls([call(), call().next(device)])
