from app.request_management.parser.parser import Parser
import app.request_management.parser.request_strategies as ParseStrat
from app.enums import InputLocation
from app.errors import ParsingError

content_functions = {
    InputLocation.NONE : ParseStrat.get_none,
    InputLocation.QUERY_DATA : ParseStrat.get_query
}

username_functions = {
    InputLocation.QUERY_DATA : ParseStrat.get_username_from_query,
}

token_functions = {
    InputLocation.NONE : ParseStrat.get_none,
}

def create_parser(expected_locations: list[str], username_location:str, token_location:str)->Parser:
    return Parser(method_fn=ParseStrat.get_method,
                  path_fn=ParseStrat.get_path,
                  query_fn=ParseStrat.get_query,
                  json_fn=ParseStrat.get_json,
                  form_fn=ParseStrat.get_form,
                  header_fn=ParseStrat.get_headers,
                  username_fn=ParseStrat.get_none,
                  token_fn=ParseStrat.get_none,
                  input_fns=ParseStrat.get_none
                  )
    
    
    # for loc in expected_locations:
    #     if loc not in InputLocation:
    #         raise ParsingError('content_type is not valid InputLocation enum')
    # if username_location not in InputLocation:
    #     raise ParsingError('username_location is not valid InputLocation enum')
    # if token_location not in InputLocation:
    #     raise ParsingError('token_location is not valid InputLocation enum')
    
    # content_fn = [content_functions.get(InputLocation(loc)) for loc in expected_locations]
    # username_fn = username_functions.get(InputLocation(username_location))
    # token_fn = token_functions.get(InputLocation(token_location))

    # return Parser(
    #     request_strategies.get_method, request_strategies.get_path,
    #     request_strategies.get_query, request_strategies.get_json,
    #     request_strategies.get_form, request_strategies.get_headers,
    #     username_fn, token_fn, content_fn
    # )
    