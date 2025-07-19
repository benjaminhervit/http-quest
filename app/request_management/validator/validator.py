from app.errors import ValidationError
from app.enums import QuestDataKey, ParserKey

class Validator:
    def __init__(self, content_fn, username_fn, token_fn):
        self.content_fn =content_fn
        self.username_fn = username_fn
        self.token_fn = token_fn
        
    def validate(self, parsed:dict, settings:dict):
        method = parsed.get(ParserKey.METHOD.value)
        expected_method = parsed.get(ParserKey.METHOD.value)
        method_is_valid = self._validate_method(method, expected_method)
        
        content = parsed.get(ParserKey.ANSWER.value)
        content_is_valid = self._validate_content(content=content, settings=settings)
        
        username = parsed.get(ParserKey.USERNAME.value)
        username_is_valid = self._validate_username(username=username, settings=settings)
        
        token = parsed.get(ParserKey.TOKEN.value)
        token_is_valid = self._validate_token(token=token, settings=settings)
        
        return method_is_valid and content_is_valid and username_is_valid and token_is_valid
    
    def _validate_method(self, method, expected_method):
        return method == expected_method
        
    def _validate_content(self, *args, **kwargs):
        return self.content_fn(args, kwargs)
    
    def _validate_username(self, *args, **kwargs):
        return self.username_fn(args, kwargs)
    
    def _validate_token(self, *args, **kwargs):
        return self.token_fn(args, kwargs)