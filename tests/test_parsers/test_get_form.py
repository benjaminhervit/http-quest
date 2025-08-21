import pytest
from flask import request
from app.utils.parser_utils import get_form


@pytest.mark.parametrize(
    "_form, expected",
    [
        ({"foo": "bar"}, {"foo": "bar"}),
    ],
)
def test_valid_get_form(app, _form, expected):
    with app.test_request_context(path="/", data=_form):
        result: dict | None = get_form(request)
        assert isinstance(result, dict)
        assert result == expected


def test_wrong_json(app):
    # when no form is send, an error is raised
    with app.test_request_context(
        path="/",
    ):
        with pytest.raises(ValueError) as excinfo:
            get_form(request)
        assert "Expected mimetype application/x-www-form-urlencoded" in str(excinfo)

    # when the right mime type but form is send, None is returned
    with app.test_request_context(
        path="/", headers={"content-type": "application/x-www-form-urlencoded"}
    ):
        assert get_form(request) is None

    # when the wrong mime type is used with form, an error is raised
    with app.test_request_context(
        path="/", headers={"content-type": "application/json"}, data={"foo": "bar"}
    ):
        with pytest.raises(ValueError) as excinfo:
            get_form(request)
        assert "Expected mimetype application/x-www-form-urlencoded" in str(excinfo)
