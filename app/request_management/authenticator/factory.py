from app.request_management.authenticator.authenticator import Authenticator
from app.enums import AuthType
from app.errors import AuthenticationError
import app.request_management.authenticator.strategies as strategies

functions = {
    AuthType.NO_AUTH : strategies.no_auth,
    AuthType.USERNAME : strategies.by_username
}

def create_authenticator(auth_type) -> Authenticator:
    if auth_type not in AuthType:
        raise AuthenticationError(f'auth_type {auth_type} is not a valid authentication enum.')
    auth_fn = functions.get(AuthType(auth_type))
    return Authenticator(auth_fn=auth_fn)