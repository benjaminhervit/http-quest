from typing import Any

def validate_mimetype(mimetype: str, expected: str) -> bool:
    if mimetype != expected:
        raise ValueError(f'Expected mimetype {expected} but found: {mimetype}')
    return True


def _validate_method(method: str, expected: str) -> bool:
    if method != expected:
        raise ValueError(f'Expected method {method} but found {expected}')
    return True


def validate_type(item: Any, _type: Any) -> bool:
    if not isinstance(item, _type):
        raise TypeError(f'Expected {_type} but got {item}')
    return True