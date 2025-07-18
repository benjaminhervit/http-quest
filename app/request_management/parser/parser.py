from flask import Request
from app.errors import ParsingError
from app.enums import StatusCode

class Parser:
    def __init__(self, content_fn:callable, username_fn:callable, token_fn:callable):
        self.content_fn = content_fn
        self.username_fn = username_fn
        self.token_fn = token_fn
    
    def parse(self, req:Request, path:str):
        try:
            return {
                'content':self.content_fn(req=req, path=path),
                'username':self.username_fn(req=req, path=path),
                'token':self.username_fn(req=req, path=path),
                'method':req.method #only one way to parse method from Request object
            }
        except ParsingError as exc:
            raise ParsingError(f'ParsingError from Parser.parse: {str(exc)}', StatusCode.BAD_REQUEST) from exc