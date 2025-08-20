import pytest
from flask import request
from app.utils.parser_utils import get_query

@pytest.mark.parametrize(
    "_path, expected",
    [
        ("/", None),
        ("/?user=test", {"user": "test"}),
        ("/?user=test&a=1", {"user": "test", "a": "1"}),
        ("/?user=test?a=1", {"user": "test?a=1"}),
    ]
)
def test_valid_get_query(app, _path, expected):
    with app.test_request_context(
        path=_path
    ):
        assert get_query(request) == expected

        
def test_catches_wrong_input():
    with pytest.raises(TypeError):
        assert get_query("/?user=test")
        
    with pytest.raises(TypeError):
        assert get_query(123)
