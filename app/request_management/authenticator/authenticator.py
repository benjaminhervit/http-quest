class Authenticator:
    def __init__(self, auth_fn:callable):
        self.auth_fn = auth_fn
        
    def authenticate(self, parsed:dict) -> bool:
        return self.auth_fn(parsed)