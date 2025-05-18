from pathlib import Path
from unittest.mock import _Call, ANY, MagicMock, call, patch

from utils import Cache
from test_utils import TestSet, parametrize

FILEPATH: str = "utils.cache"


clear_tests: TestSet = {
    "no_file": {
        "is_file": False,
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [],
        "expected_unlink_calls": [],
    },
    "file": {
        "is_file": True,
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [call.debug(ANY)],
        "expected_unlink_calls": [call()],
    },
}


@patch(f"{FILEPATH}.logging")
@patch.object(Path, "unlink")
@patch.object(Path, "is_file")
@patch.object(Path, "mkdir")
@parametrize(clear_tests)
def test_clear(
    mock_mkdir: MagicMock,
    mock_is_file: MagicMock,
    mock_unlink: MagicMock,
    mock_logging: MagicMock,
    is_file: bool,
    expected_mkdir_calls: list[_Call],
    expected_logging_calls: list[_Call],
    expected_unlink_calls: list[_Call],
) -> None:
    mock_is_file.return_value = is_file
    Cache().clear()
    mock_mkdir.assert_has_calls(expected_mkdir_calls)
    mock_logging.assert_has_calls(expected_logging_calls)
    mock_unlink.assert_has_calls(expected_unlink_calls)


read_tests: TestSet = {
    "no_file": {
        "text": "{'foo': 'bar'}",
        "is_file": False,
        "expected": {},
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [],
    },
    "file": {
        "text": '{"foo": "bar"}',
        "is_file": True,
        "expected": {"foo": "bar"},
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [call.debug(ANY)],
    },
    "empty_file": {
        "text": "",
        "is_file": True,
        "expected": {},
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [call.debug(ANY)],
    },
}


@patch(f"{FILEPATH}.logging")
@patch.object(Path, "read_text")
@patch.object(Path, "is_file")
@patch.object(Path, "mkdir")
@parametrize(read_tests)
def test_read(
    mock_mkdir: MagicMock,
    mock_is_file: MagicMock,
    mock_read_text: MagicMock,
    mock_logging: MagicMock,
    text: str,
    is_file: bool,
    expected: dict[str, str],
    expected_mkdir_calls: list[_Call],
    expected_logging_calls: list[_Call],
) -> None:
    mock_is_file.return_value = is_file
    mock_read_text.return_value = text
    assert Cache().read() == expected
    mock_mkdir.assert_has_calls(expected_mkdir_calls)
    mock_logging.assert_has_calls(expected_logging_calls)


write_tests: TestSet = {
    "no_file": {
        "is_file": False,
        "read_return": {"foo": "bar"},
        "content": {"foo": "baz"},
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [],
        "expected_write_text_calls": [],
    },
    "file": {
        "is_file": True,
        "read_return": {"foo": "bar"},
        "content": {},
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [call.debug(ANY)],
        "expected_write_text_calls": [call('{"foo": "bar"}')],
    },
    "overwrite": {
        "is_file": True,
        "read_return": {"foo": "bar"},
        "content": {"foo": "baz"},
        "expected_mkdir_calls": [call(parents=True, exist_ok=True)],
        "expected_logging_calls": [call.debug(ANY)],
        "expected_write_text_calls": [call('{"foo": "baz"}')],
    },
}


@patch(f"{FILEPATH}.logging")
@patch.object(Path, "write_text")
@patch.object(Cache, "read")
@patch.object(Path, "is_file")
@patch.object(Path, "mkdir")
@parametrize(write_tests)
def test_write(
    mock_mkdir: MagicMock,
    mock_is_file: MagicMock,
    mock_read: MagicMock,
    mock_write_text: MagicMock,
    mock_logging: MagicMock,
    is_file: bool,
    read_return: dict[str, str],
    content: dict[str, str],
    expected_mkdir_calls: list[_Call],
    expected_logging_calls: list[_Call],
    expected_write_text_calls: list[_Call],
) -> None:
    mock_is_file.return_value = is_file
    mock_read.return_value = read_return
    Cache().write(content)
    mock_mkdir.assert_has_calls(expected_mkdir_calls)
    mock_logging.assert_has_calls(expected_logging_calls)
    mock_write_text.assert_has_calls(expected_write_text_calls)
