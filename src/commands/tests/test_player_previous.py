from argparse import Namespace
from unittest.mock import MagicMock, call, patch

from src.commands import PlayerPrevious

FILEPATH: str = "src.commands.player_previous"


def test_parent_parsers() -> None:
    assert PlayerPrevious.parent_parsers() == []


@patch(f"{FILEPATH}.Spotify")
def test_init(mock_spotify: MagicMock) -> None:
    PlayerPrevious(Namespace())
    mock_spotify.assert_has_calls([call(), call().previous()])
