
from flask import Request
from app.enums import StatusCode, ParserKey
from app.errors import ParsingError

#USERNAME STRATEGIES
def get_username_from_query(*args, **kwargs):
    req:Request = kwargs.get('req')
    if req is None:
        raise ParsingError('No Request object in kwargs', code=StatusCode.SERVER_ERROR)
    content = get_answer_from_query(req=req)
    return content.get(ParserKey.USERNAME.value)

def get_username_from_path(*args, **kwargs):
    path = kwargs.get('path')
    if path is None:
        raise ParsingError('No path key in kwargs', code=StatusCode.SERVER_ERROR)
    return get_field_from_path(path=path, index=0)
    
def get_field_from_path(*args, **kwargs):
    #get args
    try:
        path:str = kwargs.get('path')
        index:int = kwargs.get('index')
    except ParsingError as exc:
        raise ParsingError(f'Could not parse kwargs: {kwargs}', code=StatusCode.BAD_REQUEST) from exc
        
    #parse
    fields = path.strip().split('/')
    if len(fields) - 1 < index:
        raise ParsingError(f'Missing index {index} in path.', code=StatusCode.BAD_REQUEST)
    
    return fields[index]

def no_username(*args, **kwargs):
    return ""
    
#CONTENT STRATEGIES
def no_content(*args, **kwargs):
    return {}

def get_answer_from_query(*args, **kwargs):
    print("START")
    req:Request = kwargs.get('req')
    key = kwargs.get('key')
    if req is None or key is None:
        raise ParsingError(f'Missing key:value in kwargs: {kwargs}. req:{req}, key:{key}', code=StatusCode.BAD_REQUEST)
    content = req.args.to_dict()
    if content is None:
        raise ParsingError('No content in query')
    print(content)
    print("END")
    return content.get('answer')

#TOKEN STRATEGIES
def no_token(*args, **kwargs):
    return ""