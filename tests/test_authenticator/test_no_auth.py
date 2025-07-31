from app.authenticator.strategies import no_auth
from app.authenticator.auth_result import AuthResult
from app.enums import ParserKey
from app.errors import AuthenticationError
from app.models import User

import pytest

@pytest.mark.parametrize("identity, expects_user, raises_exception, user_returned",
                         [({}, False, False, None),  # no username and not expected == valid
                          ({ParserKey.USERNAME: 'test'}, True, False, User(username='test')),  #u sername and expected = valid
                          ({}, True, True, User(username='test'))  # no username but expected = error
                          ])
def test_no_auth_pass_without_user(identity, expects_user, raises_exception,
                                   user_returned: User):
    if raises_exception:
        with pytest.raises(AuthenticationError):
            result = no_auth(identity, expects_user)
    else:
        result: AuthResult = no_auth(identity, expects_user)
        assert result.success is True
        if user_returned is not None:
            assert result.user.username == user_returned.username