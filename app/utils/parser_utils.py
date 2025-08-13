from flask import Request

from app.errors import ParsingError
from app.enums import StatusCode


def get_form_field(req: Request, field_name: str) -> str:
    if not isinstance(req, Request):
        raise TypeError('req is not Request obj.')
    if not isinstance(field_name, str):
        raise TypeError('field_name is not string.')
    
    form = req.form.to_dict() if req.form else None
    if not form:
        raise ParsingError('Found no form in request',
                           StatusCode.BAD_REQUEST.value)
    
    field = form.get(field_name)
    if not field:
        raise ParsingError(f'Found not field "{field_name}" in form "{form}"',
                           StatusCode.BAD_REQUEST.value)
    
    return field