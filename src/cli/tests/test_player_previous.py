from argparse import Namespace
from unittest.mock import MagicMock, call, patch

from src.cli.player_previous import PlayerPrevious

FILEPATH: str = "src.cli.player_previous"


def test_parent_parsers() -> None:
    assert PlayerPrevious.parent_parsers() == []


@patch(f"{FILEPATH}.Spotify")
def test_init(mock_spotify: MagicMock) -> None:
    PlayerPrevious(Namespace())
    mock_spotify.assert_has_calls([call(), call().previous()])
