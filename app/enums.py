from enum import Enum

class PlayerAction(str, Enum):
    ANSWER = "ANSWER"
    GET_QUEST = "GET_QUEST"

class ReqMethodType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    
class InputLocation(str, Enum):
    FORM = "FORM"
    JSON = "JSON"
    QUERY = "QUERY"
    RAW = "RAW"
    PATH = "PATH"
    HEADER = "HEADER"
    NONE = "NONE"

#keys for look up in Quest data class
class QuestDataKey(str, Enum):
    AUTH_TYPE = "AUTH_TYPE"
    CONTENT_LOCATION = "CONTENT_LOCATION"
    USERNAME_LOCATION = "USERNAME_LOCATION"
    TOKEN_LOCATION = "TOKEN_LOCATION"
    SOLVER_TYPE = "SOLVER_TYPE"
    EXPECTED_FIELDS = "EXPECTED_FIELDS"
    METHOD = "METHOD"
    ACTION_TYPE = "REQ_TYPE"
    CORRECT_ANSWER = "CORRECT_ANSWER"
    
class ParserKey(str, Enum):
    USERNAME = "username"
    METHOD = "method"
    CONTENT = "content"
    TOKEN = "token"
    
class ValidatorKeys(str, Enum):
    NONE = "NONE"
    NOT_NONE = "NOT_NONE"
    EXPECTED_FIELDS = "EXPECTED_FIELDS"
    EMPTY = "EMPTY"
    
class StatusCode(int, Enum):
    OK = 200
    ACCEPTED = 202
    BAD_REQUEST = 400
    NOT_CREATED = 999
    UNAUTHORIZED = 401
    SERVER_ERROR = 500
    
class AuthType(str, Enum):
    USERNAME = "USERNAME"
    BEARER_TOKEN = "BEARER_TOKEN"
    NO_AUTH = "NO_AUTH"
    SECRET_KEY = "X-Secret-Key"
    
class QuestState(Enum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    COMPLETED = "COMPLETED"
    
class ResponseType(Enum):
    QUEST_IS_LOCKED = "QUEST_IS_LOCKED"
    WRONG_ANSWER = "WRONG_ANSWER"
    CORRECT_ANSWER = "CORRECT_ANSWER"
    QUEST_ALREADY_COMPLETED = "QUEST_ALREADY_COMPLETED"
    GET_QUEST = "GET_QUEST"