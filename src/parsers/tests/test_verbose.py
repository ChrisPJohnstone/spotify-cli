from parsers import verbose
from test_utils import TestSet, parametrize


number_tests: TestSet = {
    "-v": {"is_top": False, "argv": ["-v"], "expected": True},
    "--verbose": {"is_top": False, "argv": ["--verbose"], "expected": True},
    "is_top_default": {"is_top": True, "argv": [], "expected": False},
}


@parametrize(number_tests)
def test_number(is_top: bool, argv: list[str], expected: bool) -> None:
    assert verbose(is_top).parse_args(argv).verbose == expected
