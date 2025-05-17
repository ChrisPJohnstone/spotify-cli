from argparse import Namespace
from unittest.mock import _Call, MagicMock, PropertyMock, call, patch

from src.cli.get_saved_tracks import GetSavedTracks
from src.type_definitions import JSONObject
from test_utils import TestSet, parametrize

FILEPATH: str = "src.cli.get_saved_tracks"


parent_parsers_tests: TestSet = {
    "20 10": {"default_limit": 20, "default_offset": 10},
    "10 20": {"default_limit": 10, "default_offset": 20},
}


@patch(f"{FILEPATH}.offset")
@patch(f"{FILEPATH}.number")
@patch.object(GetSavedTracks, "DEFAULT_OFFSET", new_callable=PropertyMock)
@patch.object(GetSavedTracks, "DEFAULT_LIMIT", new_callable=PropertyMock)
@parametrize(parent_parsers_tests)
def test_parent_parsers(
    mock_default_limit: PropertyMock,
    mock_default_offset: PropertyMock,
    mock_number: MagicMock,
    mock_offset: MagicMock,
    default_limit: int,
    default_offset: int,
) -> None:
    mock_default_limit.return_value = default_limit
    mock_default_offset.return_value = default_offset
    assert GetSavedTracks.parent_parsers() == [
        mock_number.return_value,
        mock_offset.return_value,
    ]
    mock_number.assert_called_once_with(
        default_limit,
        "Number of tracks to pull",
    )
    mock_offset.assert_called_once_with(
        default=default_offset,
        help_string="Position to start pulling from",
    )


init_tests: TestSet = {
    "simple": {
        "saved_tracks": [
            [
                {
                    "added_at": "2025-01-01",
                    "track": {
                        "artists": [
                            {"name": "Kendrick Lamar"},
                            {"name": "U2"},
                        ],
                        "name": "XXX ft. U2",
                    },
                },
                {
                    "added_at": "2024-12-31",
                    "track": {
                        "artists": [{"name": "Rag'n'Bone Man"}],
                        "name": "Human",
                    },
                },
            ],
        ],
        "max_per_request": 100,
        "args": Namespace(number=100, offset=50),
        "expected_get_saved_tracks_calls": [call(100, 50)],
        "expected_logging_calls": [call.debug("Requesting 50-150")],
        "expected_print_calls": [
            call("XXX ft. U2 by (Kendrick Lamar, U2) added 2025-01-01"),
            call("Human by (Rag'n'Bone Man) added 2024-12-31"),
        ],
    },
    "scrolling": {
        "saved_tracks": [
            [
                {
                    "added_at": "2025-01-01",
                    "track": {
                        "artists": [
                            {"name": "Kendrick Lamar"},
                            {"name": "U2"},
                        ],
                        "name": "XXX ft. U2",
                    },
                },
            ],
            [
                {
                    "added_at": "2024-12-31",
                    "track": {
                        "artists": [{"name": "Rag'n'Bone Man"}],
                        "name": "Human",
                    },
                },
            ],
        ],
        "max_per_request": 1,
        "args": Namespace(number=2, offset=7),
        "expected_get_saved_tracks_calls": [
            call(1, 7),
            call(1, 8),
        ],
        "expected_logging_calls": [
            call.debug("Requesting 7-8"),
            call.debug("Requesting 8-9"),
        ],
        "expected_print_calls": [
            call("XXX ft. U2 by (Kendrick Lamar, U2) added 2025-01-01"),
            call("Human by (Rag'n'Bone Man) added 2024-12-31"),
        ],
    },
}


@patch("builtins.print")
@patch(f"{FILEPATH}.logging")
@patch.object(GetSavedTracks, "MAX_PER_REQUEST", new_callable=PropertyMock)
@patch(f"{FILEPATH}.Spotify")
@parametrize(init_tests)
def test_init(
    mock_spotify: MagicMock,
    mock_max_per_request: PropertyMock,
    mock_logging: MagicMock,
    mock_print: MagicMock,
    saved_tracks: list[JSONObject],
    max_per_request: int,
    args: Namespace,
    expected_get_saved_tracks_calls: list[_Call],
    expected_logging_calls: list[_Call],
    expected_print_calls: list[_Call],
) -> None:
    mock_client: MagicMock = mock_spotify.return_value
    mock_get_saved_tracks: MagicMock = mock_client.get_saved_tracks
    mock_get_saved_tracks.side_effect = saved_tracks
    mock_max_per_request.return_value = max_per_request
    GetSavedTracks(args)
    mock_get_saved_tracks.assert_has_calls(expected_get_saved_tracks_calls)
    mock_logging.assert_has_calls(expected_logging_calls)
    mock_print.assert_has_calls(expected_print_calls)
