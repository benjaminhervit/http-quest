from typing import Tuple, Optional

from app.enums import ParserKey, StatusCode
from app.errors import AuthenticationError
from app.models.user import User
from app.authenticator.auth_result import AuthResult

def no_auth(identify: dict, expects_user=False) -> AuthResult:
    temp_user = None
    if expects_user:
        username = identify.get(ParserKey.USERNAME)
        if not username:
            raise AuthenticationError('Could not find user from identifity: '
                                      f'{identify}')
        temp_user = User(username=username)
    return AuthResult(success=True, user=temp_user)

def auth_by_username(identify: dict) -> AuthResult:
    username = identify.get(ParserKey.USERNAME.value)
    if username is None:
        raise AuthenticationError('Cannot authenticate when username is None',
                                  code=StatusCode.BAD_REQUEST)
    
    user = User.get_by_username(username=username)
    success = True if user else False
    return AuthResult(success=success, user=user)