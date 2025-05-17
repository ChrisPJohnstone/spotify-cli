from pytest import raises

from src.parsers import term
from test_utils import TestSet, parametrize


term_tests: TestSet = {
    "default": {
        "default": "medium_term",
        "argv": [],
        "expected": "medium_term",
    },
    "short": {
        "default": "medium_term",
        "argv": ["--term", "short_term"],
        "expected": "short_term",
    },
    "long": {
        "default": "medium_term",
        "argv": ["--term", "long_term"],
        "expected": "long_term",
    },
}


@parametrize(term_tests)
def test_term(default: str, argv: list[str], expected: int) -> None:
    assert term(default, "").parse_args(argv).term == expected


term_invalid_choice_tests: TestSet = {
    "mid": {"argv": ["--term", "mid"]},
    "3 days": {"argv": ["--term", "3 days"]},
}


@parametrize(term_invalid_choice_tests)
def test_term_invalid_choice(argv: list[str]) -> None:
    with raises(SystemExit):
        term("medium_term", "").parse_args(argv)
