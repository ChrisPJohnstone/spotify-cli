from src.parsers import verbose
from test_utils import TestSet, parametrize


number_tests: TestSet = {
    "-v": {"argv": ["-v"], "expected": True},
    "--verbose": {"argv": ["--verbose"], "expected": True},
}


@parametrize(number_tests)
def test_number(argv: list[str], expected: bool) -> None:
    assert verbose().parse_args(argv).verbose == expected
