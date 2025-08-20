import pytest
from flask import request
from app.utils.parser_utils import get_json

@pytest.mark.parametrize(
    "_json, expected",
    [
        ({"foo": "bar"}, {"foo": "bar"}),
        ({"foo": "bar", "a": "b"}, {"foo": "bar", "a": "b"})
    ]
)
def test_valid_get_json(app, _json, expected):
    with app.test_request_context(
        path="/",
        json=_json if _json else ""
    ):
        result: dict | None = get_json(request)
        assert isinstance(result, dict)
        assert result == expected

def test_wrong_json(app):
    #when no json is send, an error is raised
    with app.test_request_context(
        path="/",
    ):
        with pytest.raises(ValueError) as excinfo:
            get_json(request)
        assert 'Expected mimetype application/json' in str(excinfo)