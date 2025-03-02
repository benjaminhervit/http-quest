from enum import Enum

class MyRequestStatus(Enum):
    SUCCESS = "success"
    WRONG_METHOD = "Received wrong method"
    LEVEL_NOT_ALLOWED = 'Cannot access specified level'
    WRONG_ANSWER = 'Incorrect answer'