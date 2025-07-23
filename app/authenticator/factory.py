
from typing import Callable

from app.enums import AuthType
from app.errors import AuthenticationError
from app.authenticator.authenticator import Authenticator
import app.authenticator.strategies as strategies

auth_functions = {
    AuthType.NO_AUTH: strategies.no_auth,
    AuthType.USERNAME: strategies.by_username
}

def create_authenticator(auth_type) -> Authenticator:
    if auth_type not in AuthType:
        raise AuthenticationError(f'auth_type {auth_type} is not a valid authentication enum.')
    auth_fn: Callable | None = auth_functions.get(AuthType(auth_type))
    if not auth_fn:
        raise ValueError(f'auth_type:{auth_type} return {auth_fn} but expected Callabe.')
    return Authenticator(auth_fn)