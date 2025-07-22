from app.enums import ParserKey, StatusCode
from app.errors import AuthenticationError
from app.models.user import User

def no_auth(parsed:dict) -> bool:
    return True

def by_username(parsed:dict) -> bool:
    username = parsed.get(ParserKey.USERNAME.value)
    if username is None:
        raise AuthenticationError('Cannot authenticate when username is None', code=StatusCode.BAD_REQUEST)
    user_exists = User.get_by_username(username=username)
    if not user_exists:
        return False
    return True