from argparse import Namespace
from unittest.mock import _Call, MagicMock, call, patch

from src.commands.get_top_artists import GetTopArtists
from src.type_definitions import JSONObject
from test_utils import TestSet, parametrize


init_tests: TestSet = {
    "single": {
        "results": [(1, {"name": "Electric Light Orchestra"})],
        "expected_print_calls": [call(1, "Electric Light Orchestra")],
    },
    "multi": {
        "results": [
            (1, {"name": "Electric Light Orchestra"}),
            (2, {"name": "Wild Cherry"}),
        ],
        "expected_print_calls": [
            call(1, "Electric Light Orchestra"),
            call(2, "Wild Cherry"),
        ],
    },
}


@patch("builtins.print")
@patch.object(GetTopArtists, "_results")
@parametrize(init_tests)
def test_init(
    mock_results: MagicMock,
    mock_print: MagicMock,
    results: list[tuple[int, JSONObject]],
    expected_print_calls: list[_Call],
) -> None:
    mock_results.return_value = results
    GetTopArtists(Namespace())
    mock_print.assert_has_calls(expected_print_calls)
