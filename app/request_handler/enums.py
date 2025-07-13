from enum import Enum

class RequestParams(Enum):
    #request methods
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    
    #content types
    DATA_LOCATION = "DATA_LOCATION"
    FORM = "FORM"
    JSON = "JSON"
    QUERY = "QUERY"
    RAW = "RAW"
    PATH = "PATH"
    HEADER = "HEADER"
    
    #status codes
    STATUS_OK = 200
    STATUS_ACCEPTED = 202
    STATUS_BAD_REQUEST = 400
    STATUS_NOT_CREATED = 999
    STATUS_UNAUTHORIZED = 401
    
    #auth
    AUTH_TYPE = "AUTH_TYPE"
    AUTH_BY_USERNAME = "AUTH_BY_USERNAME"
    AUTH_BY_BEARER_TOKEN = "AUTH_BY_TOKEN"
    NO_AUTH = "NO_AUTH"
    SECRET_KEY = "X-Secret-Key"
    USERNAME_LOCATION = "USERNAME_LOCATION"
    
    #generic
    NONE = "NONE"
    

class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    
class RequestType(Enum):
    NONE = "NONE"
    FORM = "FORM"
    JSON = "JSON"
    QUERY = "QUERY"
    RAW = "RAW"
    
