from typing import Callable

class Authenticator:
    def __init__(self, auth_fn: Callable):
        self.auth_fn: Callable = auth_fn
        
    def authenticate(self, parsed: dict) -> bool:
        return self.auth_fn(parsed)