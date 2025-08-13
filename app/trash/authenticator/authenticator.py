from typing import Callable
from app.enums import ParserKey, StatusCode, QuestKey
from app.errors import AuthenticationError
from app.authenticator.auth_result import AuthResult

class Authenticator:
    def __init__(self, auth_fn: Callable):
        self.auth_fn: Callable = auth_fn
    
    def get_identity(self, parsed: dict, settings: dict) -> dict:
        username_loc = settings.get(QuestKey.USERNAME_LOC)
        if not username_loc:
            return {}
        
        username = parsed.get(username_loc)
        if not username:
            raise AuthenticationError(f'Expected username at {username_loc}'
                                      'but got None',
                                      code=StatusCode.BAD_REQUEST)
        return {
            ParserKey.USERNAME: username
        }
    
    def authenticate(self, identify: dict) -> AuthResult:
        return self.auth_fn(identify=identify)