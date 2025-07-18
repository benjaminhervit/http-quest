from typing import TypedDict

class ParsedRequest(TypedDict):
    """
    A summary of both quest settings and request data, necessary to go through parsing, validation and authentication, and game logic
    """
    #from Request
    method:str
    username: str
    answer: str | None = None
    auth_type: str
    req_action: str