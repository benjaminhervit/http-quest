import pytest
from app.utils.parser_utils import try_json_loads


def test_try_load_json_valid():
    data = '{"key": "value", "num": 42}'
    result = try_json_loads(data)
    assert isinstance(result, dict)
    assert result["key"] == "value"
    assert result["num"] == 42


def test_try_load_json_invalid():
    data = '{"key": "value", "num": 42'  # Missing closing }
    result = try_json_loads(data)
    assert result is None


def test_try_load_json_empty_string():
    data = ""
    result = try_json_loads(data)
    assert result is None


def test_try_load_json_none():
    result = try_json_loads(None)
    assert result is None


def test_try_load_json_list():
    data = "[1, 2, 3]"
    result = try_json_loads(data)
    assert isinstance(result, list)
    assert result == [1, 2, 3]


def test_try_load_json_empty_list():
    data = "1, 2, 3"
    result = try_json_loads(data, [])
    assert isinstance(result, list)
    assert result == []
