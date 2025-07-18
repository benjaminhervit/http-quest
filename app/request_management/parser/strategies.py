
from flask import Request
from app.enums import StatusCode, ParserKey
from app.errors import ParsingError

#USERNAME STRATEGIES
def get_username_from_query(*args, **kwargs):
    req:Request = kwargs.get('req')
    if req is None:
        raise ParsingError('No Request object in kwargs', code=StatusCode.SERVER_ERROR)
    content = get_content_from_query(req=req)
    return content.get(ParserKey.USERNAME)

def get_username_from_path(*args, **kwargs):
    path = kwargs.get('path')
    if path is None:
        raise ParsingError('No path key in kwargs', code=StatusCode.SERVER_ERROR)
    return get_field_from_path(path=path, index=0)
    
def get_field_from_path(*args, **kwargs):
    #get args
    path = kwargs.get('path')
    index = kwargs.get('index')
    if path is None or index is None:
        raise ParsingError('Could not find path or index for path field.', code=StatusCode.BAD_REQUEST)
    
    #parse
    fields = path.strip().split('/')
    if len(fields) - 1 > index:
        raise ParsingError(f'Missing index {index} in path.', code=StatusCode.BAD_REQUEST)
    
    return fields[index]

def no_username(*args, **kwargs):
    return ""
    
#CONTENT STRATEGIES
def no_content(*args, **kwargs):
    return {}

def get_content_from_query(req:Request):
    content = req.args.to_dict()
    if content is None:
        raise ParsingError('No content in query')
    return content

#TOKEN STRATEGIES
def no_token(*args, **kwargs):
    return ""