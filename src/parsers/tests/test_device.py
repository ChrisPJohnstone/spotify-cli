from parsers import device
from test_utils import TestSet, parametrize


device_tests: TestSet = {
    "default": {"argv": [], "expected": []},
    "--device": {"argv": ["Speaker"], "expected": ["Speaker"]},
}


@parametrize(device_tests)
def test_device(argv: list[str], expected: list[str]) -> None:
    assert device().parse_args(argv).device == expected
