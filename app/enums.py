from enum import Enum

class ReqMethodType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class QuestKey(str, Enum):
    METHOD_DATA = "METHOD_DATA"
    
    USERNAME = "username"
    USERNAME_LOC = "USERNAME_LOC"
    
    ANSWER = "answer"
    ANSWER_KEY = "ANSWER_KEY"
    ANSWER_LOC = "ANSWER_LOC"
    SOLUTION_FN_KEY = "SOLUTION_FN"
    
    TOKEN = "token"
    TOKEN_LOC = "TOKEN_LOC"
    
    FORM_KEYS = "FORM_KEYS"
    
    JSON_KEYS = "JSON_KEYS"
    
    HEADERS_KEYS = "HEADERS_KEYS"
    
    INPUT_LOC = "INPUT_LOC"
    
    QUERY_KEYS = "QUERY_KEYS"
    
    AUTH_TYPE = "AUTH_TYPE"
    
    NONE = "NONE"
    
class ParserKey(str, Enum):
    NONE = "NONE"
    
    #USERNAME = "username"
    #USERNAME_LOC = "USERNAME_LOC"
   
    METHOD = "method"
    METHOD_DATA = "METHOD_DATA"
    
    #ANSWER = "answer"
    #ANSWER_KEY = "ANSWER_KEY"
    #SOLUTION_FN_KEY = "SOLUTION_FN"
    
    #TOKEN = "token"
    #TOKEN_LOC = "TOKEN_LOC"
    
    #FORM_KEYS = "FORM_KEYS"
    FORM_DATA = "FORM_DATA"
    
    #JSON_KEYS = "JSON_KEYS"
    JSON_DATA = "JSON_DATA"
    
    #HEADERS_KEYS = "HEADERS_KEYS"
    HEADERS_DATA = "HEADERS_DATA"
    
    #AUTH_TYPE = "AUTH_TYPE"
    
    #INPUT_LOC = "INPUT_LOC"
    #INPUT_DATA = "INPUT_DATA"
    
    #QUERY_KEYS = "QUERY_KEYS"
    QUERY_DATA = "QUERY_DATA"
    
    PATH_DATA = "PATH_DATA"
    
    #NONE = "NONE"

class QuestExecutionStrategy(str, Enum):
    NONE = "NONE"
    ACCEPT_QUEST = "ACCEPT_QUEST"


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