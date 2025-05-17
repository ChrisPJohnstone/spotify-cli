from argparse import Namespace
from unittest.mock import MagicMock, call, patch

from src.commands import LogOut

FILEPATH: str = "src.commands.logout"


def test_parent_parsers() -> None:
    assert LogOut.parent_parsers() == []


@patch(f"{FILEPATH}.Spotify")
def test_init(mock_spotify: MagicMock) -> None:
    LogOut(Namespace())
    mock_spotify.assert_has_calls([call(), call().clear_cache()])
