from app.errors import ParsingError
from app.enums import StatusCode

def none_quest(*args, **kwargs):
    return True

def single_input_validator(*args, **kwargs):
    user_input = kwargs.get('user_input')
    expected = kwargs.get('validation_data')
    if user_input is None or expected is None:
        raise ParsingError(f'missing keys in kwargs: {kwargs}. input:{user_input}, exp:{expected}', code=StatusCode.SERVER_ERROR)
    
    return user_input == expected