import pytest
from flask import request
from app.utils.parser_utils import get_headers

@pytest.mark.parametrize(
    "_headers, expected",
    [
        (None, {"host": "localhost"}),
        ({"authorization": "test"}, {"authorization": "test"}),
    ]
)
def test_valid_get_headers(app, _headers, expected):
    with app.test_request_context(
        path="/",
        headers=_headers
    ):
        result: dict | None = get_headers(request)
        assert isinstance(result, dict)
        assert all(item in result.items() for item in expected.items())

def test_catches_wrong_input(app):
    with pytest.raises(TypeError):
        assert get_headers({"authorization": "test"})
