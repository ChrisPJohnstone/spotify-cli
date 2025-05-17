from src.utils import split_uri
from test_utils import TestSet, parametrize


split_uri_tests: TestSet = {
    "localhost": {
        "uri": "http://localhost:8080",
        "expected": ("http", "localhost", 8080),
    },
    "172.0.0.1": {
        "uri": "https://172.0.0.1:80",
        "expected": ("https", "172.0.0.1", 80),
    },
}


@parametrize(split_uri_tests)
def test_split_uri(uri: str, expected: tuple[str, str, int]) -> None:
    assert split_uri(uri) == expected
