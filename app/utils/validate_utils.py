from typing import Any
from flask import Request

from app.errors import ParsingError


def validate_mimetype(mimetype: str, expected: str) -> bool:
    if mimetype != expected:
        raise ValueError(f"Expected mimetype {expected} but found: {mimetype}. Maybe you can find what you need here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type")
    return True


def _validate_method(method: str, expected: str) -> bool:
    if method != expected:
        raise ValueError(f"Expected method {method} but found {expected}")
    return True


def validate_content_is_json(req: Request) -> bool:
    content_type = req.content_type
    if content_type != "application/json":
        raise ValueError(f"Expected content-type: application/json but found: {content_type}. Maybe this can help you: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type")
    return True

    
def validate_req_has_data(req: Request) -> bool:
    print(req.content_length)
    if req.content_length is None:
        return True
    if req.content_length <= 0:
        raise ParsingError(f"Did not find any data with the request. Content_length is {req.content_length}")
    return True


def validate_type(item: Any, _type: Any) -> bool:
    if not isinstance(item, _type):
        raise TypeError(f"Expected {_type} but got {item}")
    return True


def validate_headers_obj(headers):
    try:
        # check if object is iterable with k,v
        iter(headers.items())
    except Exception as exc:
        raise TypeError("Expected headers-like object with .items()") from exc
