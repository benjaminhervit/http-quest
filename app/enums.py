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

#keys for look up in Quest data class
class ParsingKey(str, Enum): 
    AUTH_TYPE = "AUTH_TYPE"
    EXPECTED_FIELDS = "EXPECTED_FIELDS" 
    USERNAME = "USERNAME"
    ANSWER = "ANSWER"
    METHOD = "METHOD"
    ACTION_TYPE = "REQ_TYPE"
    CORRECT_ANSWER = "CORRECT_ANSWER"
    
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