class Authenticator:
    def __init__(self, auth_fn:callable):
        self.auth_fn = auth_fn
        
    def authenticate(self, *args, **kwargs) -> bool:
        return self.auth_fn(*args, **kwargs)