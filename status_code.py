from enum import Enum
#inspired by https://www.w3.org/Protocols/HTTP/HTRESP.html
class StatusCode(Enum):
    OK = 200
    ACCEPTED = 202
    BAD_REQUEST = 400
    NOT_CREATED = 999