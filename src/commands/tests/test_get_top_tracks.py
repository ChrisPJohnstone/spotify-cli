from argparse import Namespace
from unittest.mock import _Call, MagicMock, call, patch

from commands import GetTopTracks
from type_definitions import JSONObject
from test_utils import TestSet, parametrize


init_tests: TestSet = {
    "single": {
        "results": [
            (
                1,
                {
                    "name": "May Sinde",
                    "artists": [{"name": "Tropavibes"}, {"name": "Val Ortiz"}],
                },
            ),
        ],
        "expected_print_calls": [
            call(f"1 {'May Sinde':<50}Tropavibes, Val Ortiz"),
        ],
    },
    "multi": {
        "results": [
            (
                1,
                {
                    "name": "May Sinde",
                    "artists": [{"name": "Tropavibes"}, {"name": "Val Ortiz"}],
                },
            ),
            (
                2,
                {"name": "Red Kingdom", "artists": [{"name": "Tech N9ne"}]},
            ),
        ],
        "expected_print_calls": [
            call(f"1 {'May Sinde':<50}Tropavibes, Val Ortiz"),
            call(f"2 {'Red Kingdom':<50}Tech N9ne"),
        ],
    },
}


@patch("builtins.print")
@patch.object(GetTopTracks, "_results")
@parametrize(init_tests)
def test_init(
    mock_results: MagicMock,
    mock_print: MagicMock,
    results: list[tuple[int, JSONObject]],
    expected_print_calls: list[_Call],
) -> None:
    mock_results.return_value = results
    GetTopTracks(Namespace(number=1, offset=0))
    mock_print.assert_has_calls(expected_print_calls)
