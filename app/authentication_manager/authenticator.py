from flask import Request
from app.utils import parser_utils
from app.errors import ParsingError, AuthenticationError
from app.enums import StatusCode
from app.models import User

def authenticate(req: Request) -> bool:
    username = parser_utils.get_auth_username(req)
    if not username:
        raise ParsingError('Validator received no user.'
                           'Check if you have made your authorization'
                           'header correctly.',
                           StatusCode.BAD_REQUEST.value)
    if not User.user_exists(username):
        raise AuthenticationError((f'Username {username} not recognized.'
                                   'Check spelling or sign up at'
                                   '/auth/register'),
                                  StatusCode.BAD_REQUEST.value)

    return True