from app.request_management.parser.parser import Parser
import app.request_management.parser.strategies as strategies
from app.enums import InputLocation
from app.errors import ParsingError

content_functions = {
    InputLocation.NONE : strategies.no_content,
    InputLocation.QUERY : strategies.get_answer_from_query
}

username_functions = {
    InputLocation.PATH : strategies.get_username_from_path,
    InputLocation.QUERY : strategies.get_username_from_query,
}

token_functions = {
    InputLocation.NONE : strategies.no_token,
}

def create_parser(content_location:str, username_location:str, token_location:str)->Parser:
    if content_location not in InputLocation:
        raise ParsingError('content_type is not valid InputLocation enum')
    if username_location not in InputLocation:
        raise ParsingError('username_location is not valid InputLocation enum')
    if token_location not in InputLocation:
        raise ParsingError('token_location is not valid InputLocation enum')
    
    content_fn = content_functions.get(InputLocation(content_location))
    username_fn = username_functions.get(InputLocation(username_location))
    token_fn = token_functions.get(InputLocation(token_location))
    return Parser(answer_fn=content_fn, username_fn=username_fn, token_fn=token_fn)
    