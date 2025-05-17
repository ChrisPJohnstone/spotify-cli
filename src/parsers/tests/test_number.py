from parsers import number
from test_utils import TestSet, parametrize


number_tests: TestSet = {
    "default": {"default": 3, "argv": [], "expected": 3},
    "-n": {"default": 3, "argv": ["-n", "10"], "expected": 10},
    "--number": {"default": 3, "argv": ["--number", "30"], "expected": 30},
}


@parametrize(number_tests)
def test_number(default: int, argv: list[str], expected: int) -> None:
    assert number(default, "").parse_args(argv).number == expected
