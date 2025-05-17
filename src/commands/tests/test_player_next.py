from argparse import Namespace
from unittest.mock import MagicMock, call, patch

from src.commands.player_next import PlayerNext

FILEPATH: str = "src.commands.player_next"


def test_parent_parsers() -> None:
    assert PlayerNext.parent_parsers() == []


@patch(f"{FILEPATH}.Spotify")
def test_init(mock_spotify: MagicMock) -> None:
    PlayerNext(Namespace())
    mock_spotify.assert_has_calls([call(), call().next()])
