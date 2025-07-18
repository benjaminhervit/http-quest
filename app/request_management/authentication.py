from app.models.user import User
from app.enums import AuthType, StatusCode, QuestDataKey
from app.request_management.parser.parsed_request import ParsedRequest
from app.errors import AuthenticationError

def auth(parsed:ParsedRequest):
    auth_type = parsed.get(QuestDataKey.AUTH_TYPE.value)
    if auth_type is None:
        raise AuthenticationError('No authentication type given. Talk with developer.', code=StatusCode.SERVER_ERROR)
    
    if auth_type == AuthType.NO_AUTH:
        return True
    elif auth_type == AuthType.USERNAME:
        username = parsed.get(QuestDataKey.USERNAME.value)
        if username is None:
            raise AuthenticationError(f'Cannot validate by username without a username. Check that username is send with correct key and right location (form/json/query/path...)', code=StatusCode.BAD_REQUEST)
        
        if User.get_by_username(username) is None:
            raise AuthenticationError(f'Username {username} is not registered. Check spelling or register at the landing page.', code=StatusCode.BAD_REQUEST)
        return True
    
    #something did not go as planned
    return False