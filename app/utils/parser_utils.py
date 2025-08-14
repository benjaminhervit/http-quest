from flask import Request
from typing import Callable
import collections.abc as colabc

from app.errors import ParsingError
from app.enums import StatusCode


def get_auth_username(req: Request):
    return get_field_from_request_data(req, "authorization", get_headers)


def get_view_args(req: Request):
    return req.view_args if req.view_args else None


def get_headers(req: Request) -> dict | None:
    return {k.lower(): v for k, v in req.headers.items()}


def get_json(req: Request) -> dict | None:
    return req.get_json() if req.json else None


def get_form(req: Request) -> dict | None:
    return req.form.to_dict() if req.form else None


def get_field_from_request_data(
    req: Request, field_name: str, parsing_method: Callable
) -> str:
    if not isinstance(req, Request):
        raise TypeError("req is not Request obj.")
    if not isinstance(field_name, str):
        raise TypeError("field_name is not string.")
    if not isinstance(parsing_method, colabc.Callable):
        raise TypeError("parsing_method is not Callable.")

    data: dict | None = parsing_method(req=req)
    if not data:
        raise ParsingError(
            "Found no data in request in expected format", StatusCode.BAD_REQUEST.value
        )

    field: str | None = data.get(field_name)
    if not field:
        raise ParsingError(
            f"Did not find field {field_name} in data: {data}",
            StatusCode.BAD_REQUEST.value,
        )

    return field
