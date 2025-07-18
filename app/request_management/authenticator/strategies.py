from app.enums import ParserKey, StatusCode
from app.errors import AuthenticationError
from app.models.user import User

def no_auth(*args, **kwargs) -> bool:
    return True

def by_username(*args, **kwargs) -> bool:
    username = kwargs.get(ParserKey.USERNAME)
    if username is None:
        raise AuthenticationError('Cannot authenticate when username is None', code=StatusCode.BAD_REQUEST)
    user_exists = User.get_by_username(username=username)
    if not user_exists:
        return False
    return True