from app.authenticator.factory import create_authenticator
from app.authenticator.auth_result import AuthResult
from app.enums import AuthType
from app.errors import AuthenticationError
from app.authenticator.strategies import no_auth

import pytest

def test_no_auth_factory_always_auth():
    auth = create_authenticator(AuthType.NO_AUTH)
    result: AuthResult = auth.authenticate({})
    assert result.success is True
    assert result.user is None
    