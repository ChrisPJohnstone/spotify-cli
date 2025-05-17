from argparse import Namespace
from unittest.mock import _Call, MagicMock, PropertyMock, call, patch

from commands._get_top import GetTop
from type_definitions import JSONObject
from test_utils import TestSet, parametrize

FILEPATH: str = "commands._get_top"

type ResultsReturn = tuple[int, JSONObject]


parent_parsers_tests: TestSet = {
    "1": {
        "default_limit": 20,
        "default_offset": 10,
        "default_term": "short_term",
    },
    "2": {
        "default_limit": 10,
        "default_offset": 20,
        "default_term": "long_term",
    },
}


@patch(f"{FILEPATH}.term")
@patch(f"{FILEPATH}.offset")
@patch(f"{FILEPATH}.number")
@patch.object(GetTop, "DEFAULT_TERM", new_callable=PropertyMock)
@patch.object(GetTop, "DEFAULT_OFFSET", new_callable=PropertyMock)
@patch.object(GetTop, "DEFAULT_LIMIT", new_callable=PropertyMock)
@parametrize(parent_parsers_tests)
def test_parent_parsers(
    mock_default_limit: PropertyMock,
    mock_default_offset: PropertyMock,
    mock_default_term: PropertyMock,
    mock_number: MagicMock,
    mock_offset: MagicMock,
    mock_term: MagicMock,
    default_limit: int,
    default_offset: int,
    default_term: int,
) -> None:
    mock_default_limit.return_value = default_limit
    mock_default_offset.return_value = default_offset
    mock_default_term.return_value = default_term
    assert GetTop.parent_parsers() == [
        mock_number.return_value,
        mock_offset.return_value,
        mock_term.return_value,
    ]
    mock_number.assert_called_once_with(
        default_limit,
        "Number of tracks to pull",
    )
    mock_offset.assert_called_once_with(
        default_offset,
        "Rank to start pulling from",
    )
    mock_term.assert_called_once_with(
        default=default_term,
        help_string="Over what time frame affinity is computed",
    )


results_tests: TestSet = {
    "simple": {
        "args": Namespace(number=2, offset=5, term="short"),
        "item_type": "artists",
        "max_per_request": 50,
        "get_top_returns": [[(1, {}), (2, {})]],
        "expected": [(1, {}), (2, {})],
        "expected_logging_calls": [call.debug("Requesting artists 5-7")],
        "expected_get_top_calls": [call("artists", "short", 2, 5)],
    },
    "scrolling": {
        "args": Namespace(number=2, offset=5, term="short"),
        "item_type": "artists",
        "max_per_request": 1,
        "get_top_returns": [[(1, {})], [(2, {})]],
        "expected": [(1, {}), (2, {})],
        "expected_logging_calls": [
            call.debug("Requesting artists 5-6"),
            call.debug("Requesting artists 6-7"),
        ],
        "expected_get_top_calls": [
            call("artists", "short", 1, 5),
            call("artists", "short", 1, 6),
        ],
    },
}


@patch(f"{FILEPATH}.logging")
@patch(f"{FILEPATH}.Spotify")
@patch.object(GetTop, "MAX_PER_REQUEST", new_callable=PropertyMock)
@patch.object(GetTop, "item_type", new_callable=PropertyMock)
@patch.object(GetTop, "args", new_callable=PropertyMock)
@patch.object(GetTop, "__init__", new=MagicMock(return_value=None))
@patch.object(GetTop, "__abstractmethods__", set())
@parametrize(results_tests)
def test_results(
    mock_args: PropertyMock,
    mock_item_type: PropertyMock,
    mock_max_per_request: PropertyMock,
    mock_spotify: MagicMock,
    mock_logging: MagicMock,
    args: Namespace,
    item_type: str,
    max_per_request: int,
    get_top_returns: list[list[ResultsReturn]],
    expected: list[ResultsReturn],
    expected_logging_calls: list[_Call],
    expected_get_top_calls: list[_Call],
) -> None:
    mock_args.return_value = args
    mock_max_per_request.return_value = max_per_request
    mock_item_type.return_value = item_type
    mock_client: MagicMock = mock_spotify.return_value
    mock_get_top: MagicMock = mock_client.get_top
    mock_get_top.side_effect = get_top_returns
    unit: GetTop = GetTop()  # type: ignore
    assert list(unit._results()) == expected
    mock_logging.assert_has_calls(expected_logging_calls)
    mock_get_top.assert_has_calls(expected_get_top_calls)
