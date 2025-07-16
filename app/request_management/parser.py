from flask import Request
from app.errors import ParsingError, ValidationError
from app.enums import InputLocation, ParsingKey, StatusCode, AuthType, ReqMethodType, QuestAction
from app.request_management.parsed_request import ParsedRequest

def parse(req:Request, quest_settings:dict, path:str)->ParsedRequest:
    if quest_settings is None or req is None:
        raise ParsingError('Request or Quest settings are missing. Talk with developer', code=StatusCode.SERVER_ERROR)
    
    parsed:ParsedRequest = ParsedRequest()
    
    #PARSE METHOD
    method = _get_method(req)
    _method_is_valid(method, quest_settings.keys())
    parsed[ParsingKey.METHOD.value] = method
    
    #GET EXPECTED SETTINGS
    settings:dict = _get_req_settings(method, quest_settings)
    parsed[ParsingKey.AUTH_TYPE.value] = _get_auth_type(settings)
    parsed[ParsingKey.ACTION_TYPE.value] = _get_req_type(settings)
    if parsed[ParsingKey.ACTION_TYPE.value] == QuestAction.ANSWER:
        parsed[ParsingKey.CORRECT_ANSWER.value] = _get_correct_answer(settings)

    #PARSE EXPECTED FIELDS
    expected_fields = _get_expected_fields(settings)
    for key in expected_fields:
        location:str = _get_location(key, settings)
        parsed[key] = _get_field(ParsingKey(key), InputLocation(location), req, path) #should be able to cast to enum now without worries

    return parsed

#SETTINGS FUNCTIONS
def _get_correct_answer(settings:dict):
    correct_answer = settings.get(ParsingKey.CORRECT_ANSWER.value)
    if correct_answer is None:
        raise ParsingError('Could not find correct answer to quest. Dev issue', code=StatusCode.SERVER_ERROR)
    return correct_answer

def _get_location(key:str, settings:dict):
    location:str = settings.get(key)
    if location is None or location not in InputLocation:
        raise ValidationError(f'Location {location} for field {key} is not valid. Check your request or talk with the developer?', code=StatusCode.BAD_REQUEST)
    return location

def _get_auth_type(settings:dict) -> str:
    auth_type = settings.get(ParsingKey.AUTH_TYPE.value)
    if auth_type is None:
        raise ParsingError('Could not find authentication type in settings. Talk with developer', code=StatusCode.SERVER_ERROR)
    if auth_type not in AuthType:
        raise ParsingError(f'Quest is trying to use invalid authentication {auth_type}. Ask the quest developer to get their things straight.', code=StatusCode.SERVER_ERROR)
    return auth_type

def _get_req_type(settings:dict) -> str:
    req_type:str = settings.get(ParsingKey.ACTION_TYPE.value)
    if req_type is None:
        raise ParsingError('Could not find request type in settings. Talk with developer', code=StatusCode.SERVER_ERROR)
    if req_type not in QuestAction:
        raise ParsingError(f'Quest is trying to use invalid req type: {req_type}. Ask the quest developer to get their things straight.', code=StatusCode.SERVER_ERROR)
    return req_type

def _get_req_settings(method:str, quest_settings:dict):
    #get the settings for the used request method
    settings = quest_settings.get(method)
    if settings is None:
        raise ParsingError(f'There is not settings for the method {method}', code=StatusCode.SERVER_ERROR)
    return settings

#METHOD FUNCTIONS
def _get_method(req:Request):
    #get method
    method = req.method
    if method is None:
        raise ParsingError('Could not find method for request', code=StatusCode.SERVER_ERROR)
    return method

def _method_is_valid(method:str, allowed:list[str]):
    if method not in allowed:
        raise ValidationError (f'method {method} is not valid for this quest', code=StatusCode.BAD_REQUEST)
    return True


#EXPECTED FIELDS FUNCTIONS
def _get_expected_fields(settings:dict):
    expected_fields:list[str] = settings.get(ParsingKey.EXPECTED_FIELDS.value)
    valid_fields = [e.value for e in ParsingKey]
    if not set(expected_fields).issubset(set(valid_fields)):
        raise ParsingError(f'Quest is expecting invalid field(s): {expected_fields}. Valid fields: {valid_fields}. Reach out to dev/instructor', code=StatusCode.SERVER_ERROR)
    return expected_fields

def _get_field(key:ParsingKey, location:InputLocation, req:Request, path:str):
    field = None
    if location == InputLocation.PATH:
        field = _get_field_from_path(key, path)
    elif location == InputLocation.QUERY:
        field = _get_field_from_query(key, req)
    
    if field is None:
        raise ValidationError(f'key {key.value} in {location} was empty.', code=StatusCode.BAD_REQUEST)
    return field

def _get_field_from_query(key:ParsingKey, req:Request):
    try:
        fields = req.args.to_dict()
        return fields.get(key.value.lower())
    except ParsingError as exc:
        raise ParsingError(f'Could not find {key.value} in query') from exc

def _get_field_from_path(key:ParsingKey, path:str):
    try:
        fields = path.strip().split('/')
        if key == ParsingKey.USERNAME:
            return fields[0]
    except IndexError as exc:
        raise ParsingError(f'Missing {key.value} in path.', StatusCode.BAD_REQUEST) from exc