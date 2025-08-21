import pytest
from flask import request
from app.utils.parser_utils import (
    get_field_from_request_data,
    get_query,
    get_headers,
    get_json,
)
from app.errors import ParsingError


@pytest.mark.parametrize(
    "_path, _query, _method, _json, _form, _headers, _func, field_name, expected",
    [
        # query test
        ("/", "?username=test", "GET", None, None, None, get_query, "username", "test"),
        ("/", "?a=b&c=d", "GET", None, None, None, get_query, "a", "b"),
        ("/", "?a=b&c=d", "GET", None, None, None, get_query, "c", "d"),
        ("/", "?a=b?c=d", "GET", None, None, None, get_query, "a", "b?c=d"),
        ("/", "?a=b?c=d", "GET", None, None, None, get_query, "c", ParsingError),
        ("/", "a=b&c=d", "GET", None, None, None, get_query, "c", ParsingError),
        ("/", "", "GET", None, None, None, get_query, "c", ParsingError),
        # headers
        (
            "/",
            "",
            "GET",
            None,
            None,
            {"authorization": "test"},
            get_headers,
            "authorization",
            "test",
        ),
        (
            "/",
            "",
            "GET",
            None,
            None,
            {"Authorization": "test"},
            get_headers,
            "authorization",
            "test",
        ),
        (
            "/",
            "",
            "GET",
            None,
            None,
            {"Authorization": "test"},
            get_headers,
            "Authorization",
            "test",
        ),
        (
            "/",
            "",
            "GET",
            None,
            None,
            {"abs": "test"},
            get_headers,
            "Authorization",
            ParsingError,
        ),
        ("/", "", "GET", None, None, None, get_headers, "Authorization", ParsingError),
        # json
        ("/", "", "GET", {"foo": "bar"}, None, None, get_json, "foo", "bar"),  #  valid
        (
            "/",
            "",
            "GET",
            {"foo": "bar", "a": "b"},
            None,
            None,
            get_json,
            "a",
            "b",
        ),  #  valid
        (
            "/",
            "",
            "GET",
            {"foo": None},
            None,
            None,
            get_json,
            "foo",
            ParsingError,
        ),  #  wrong json
        (
            "/",
            "",
            "GET",
            '{"foo": bar}',
            None,
            None,
            get_json,
            "foo",
            TypeError,
        ),  #  wrong json
        (
            "/",
            "",
            "GET",
            {"foo": "bar"},
            None,
            {"content-type": "abc"},
            get_json,
            "foo",
            ValueError,
        ),  #  wrong headers
        (
            "/",
            "",
            "GET",
            None,
            {"foo": "bar"},
            None,
            get_json,
            "foo",
            ValueError,
        ),  # form instead of json
    ],
)
def test_get_field(
    app, _path, _query, _method, _json, _form, _headers, _func, field_name, expected
):
    with app.test_request_context(
        path=_path + _query, method=_method, headers=_headers, json=_json, data=_form
    ):

        expects_error = expected in [ParsingError, ValueError, TypeError]
        if expects_error:
            with pytest.raises(expected):
                get_field_from_request_data(request, field_name, _func)
        else:
            result: str | None = get_field_from_request_data(request, field_name, _func)
            assert result == expected
