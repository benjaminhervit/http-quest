from flask import Request
from typing import Callable, Any
import collections.abc as colabc
from collections.abc import Mapping
import json

from app.errors import ParsingError
from app.enums import StatusCode
from app.utils import validate_utils


def try_json_loads(s, default=None):
    if not s:
        return default
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return default


def get_auth_username(req: Request):
    validate_utils.validate_type(req, Request)
    return get_field_from_request_data(req, "authorization", get_headers)


def get_headers(req: Request) -> dict | None:
    validate_utils.validate_type(req, Request)
    validate_utils.validate_headers_obj(req.headers)
    try:
        headers = {k.lower(): v for k, v in req.headers.items()}
    except TypeError as exc:
        raise TypeError('Could not parse headers. Format corrupted.') from exc
    return headers


def get_json(req: Request) -> dict | None:
    validate_utils.validate_type(req, Request)
    validate_utils.validate_mimetype(req.mimetype, "application/json")
    return req.get_json() if req.json else None


def get_form(req: Request) -> dict | None:
    validate_utils.validate_type(req, Request)
    validate_utils.validate_mimetype(req.mimetype, "application/x-www-form-urlencoded")
    return req.form.to_dict() if req.form else None


def get_query(req: Request) -> dict | None:
    validate_utils.validate_type(req, Request)
    return req.args.to_dict() if req.args else None


def get_field_from_request_data(req: Request, field_name: str,
                                parsing_method: Callable) -> str:

    validate_utils.validate_type(req, Request)
    if not isinstance(parsing_method, colabc.Callable):
        raise TypeError("parsing_method is not Callable.")

    if not isinstance(field_name, str):
        raise TypeError("field_name is not string.")

    data: dict | None = parsing_method(req=req)
    if not data:
        raise ParsingError(
            "Found no data in request in expected format", StatusCode.BAD_REQUEST.value
        )

    if not isinstance(data, dict):
        raise TypeError(f'req data format is not valid: {data}',
                        StatusCode.BAD_REQUEST.value)

    field: str | None = data.get(field_name.lower())
    if not field:
        raise ParsingError(
            f"Did not find field {field_name} in data: {data}",
            StatusCode.BAD_REQUEST.value,
        )

    return field
