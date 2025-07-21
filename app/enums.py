from enum import Enum

class ReqMethodType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

#keys for look up in Quest data class
class QuestDataKey(str, Enum):
    AUTH_TYPE = "AUTH_TYPE"
    CONTENT_LOCATION = "CONTENT_LOCATION"
    USERNAME_LOCATION = "USERNAME_LOCATION"
    TOKEN_LOCATION = "TOKEN_LOCATION"
    QUEST_VALIDATOR_TYPE = "QUEST_VALIDATOR_TYPE"
    EXPECTED_FIELDS = "EXPECTED_FIELDS"
    METHOD = "METHOD"
    ACTION_TYPE = "REQ_TYPE"
    CORRECT_ANSWER = "CORRECT_ANSWER"
    
class ParserKey(str, Enum):
    USERNAME = "username"
    USERNAME_LOC = "USERNAME_LOC"
   
    METHOD = "method"
    # METHOD_DATA = "METHOD_DATA"
    
    ANSWER = "answer"
    ANSWER_KEY = "ANSWER_KEY"
    
    TOKEN = "token"
    TOKEN_LOC = "TOKEN_LOC"
    
    METHOD_DATA = "ALLOWED_REQ_METHODS"
    
    FORM_KEYS = "FORM_KEYS"
    FORM_DATA = "FORM_DATA"
    
    JSON_KEYS = "JSON_KEYS"
    JSON_DATA = "JSON_DATA"
    
    HEADERS_KEYS = "HEADERS_KEYS"
    HEADERS_DATA = "HEADERS_DATA"
    
    AUTH_TYPE = "AUTH_TYPE"
    
    INPUT_LOC = "INPUT_LOC"
    
    QUERY_KEYS = "QUERY_KEYS"
    QUERY_DATA = "QUERY_DATA"
    
    PATH_DATA = "PATH_DATA"
    
    NONE = "NONE"
    
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
    NONE = "NONE"
    
class QuestState(Enum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    CLOSED = "CLOSED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    
#  Helper enum to validate values in different contexts
class InputLocation(str, Enum):
    METHOD = ParserKey.METHOD.value
    FORM_DATA = ParserKey.FORM_DATA.value
    JSON_DATA = ParserKey.JSON_DATA.value
    QUERY_DATA = ParserKey.QUERY_DATA.value
    PATH_DATA = ParserKey.PATH_DATA.value
    HEADERS_DATA = ParserKey.HEADERS_DATA.value
    NONE = ParserKey.NONE.value