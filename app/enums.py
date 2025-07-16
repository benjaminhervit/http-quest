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

# class RequestEnums(Enum):
#     #request methods
#     METHOD_TYPE = "METHOD_TYPE"
#     GET = "GET"
#     POST = "POST"
#     PUT = "PUT"
#     DELETE = "DELETE"

#     #content/body
#     BODY_TYPE = "BODY_TYPE"
#     FORM = "FORM"
#     JSON = "JSON"
#     QUERY = "QUERY"
#     RAW = "RAW"
#     PATH = "PATH"
#     HEADER = "HEADER"

#     #content fields
#     EXPECTED_FIELDS_IN_BODY = "EXPECTED_FIELDS_IN_BODY"
#     ANSWER_FIELD = "ANSWER_FIELD"
#     USERNAME_FIELD = "USERNAME_FIELD"

#     #status codes
#     STATUS_OK = 200
#     STATUS_ACCEPTED = 202
#     STATUS_BAD_REQUEST = 400
#     STATUS_NOT_CREATED = 999
#     STATUS_UNAUTHORIZED = 401

#     #auth
#     AUTH_TYPE = "AUTH_TYPE"
#     AUTH_BY_USERNAME = "AUTH_BY_USERNAME"
#     AUTH_BY_BEARER_TOKEN = "AUTH_BY_TOKEN"
#     NO_AUTH = "NO_AUTH"
#     SECRET_KEY = "X-Secret-Key"

#     #username
#     USERNAME_LOCATION = "USERNAME_LOCATION"
#     UNREGISTERED_USER = "Mysterious_Unknown_Player"

#     #request type
#     REQUEST_TYPE = "REQUEST_TYPE"
#     REQUEST_IS_ANSWER = "REQUEST_IS_ANSWER"
#     REQUEST_IS_GET_QUEST = "REQUEST_IS_GET_QUEST"

#     #generic
#     NONE = "NONE"