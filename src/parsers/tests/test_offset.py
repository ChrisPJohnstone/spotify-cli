from src.parsers import offset
from test_utils import TestSet, parametrize


offset_tests: TestSet = {
    "default": {"default": 2, "argv": [], "expected": 2},
    "--offset": {"default": 2, "argv": ["--offset", "17"], "expected": 17},
}


@parametrize(offset_tests)
def test_offset(default: int, argv: list[str], expected: int) -> None:
    assert offset(default, "").parse_args(argv).offset == expected
