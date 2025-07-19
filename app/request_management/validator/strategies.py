from app.errors import ValidationError
from app.enums import StatusCode


def no_data_expected(*args, **kwargs):
    has_data = args is not None or kwargs is not None 
    if has_data:
        raise ValidationError('No data expected but found content',
                              code=StatusCode.BAD_REQUEST)
    return True


def none_method(*args, **kwargs):
    return True


def any_data_expected(*args, **kwargs):
    no_data = args is None and kwargs is None 
    if no_data:
        raise ValidationError('Expected any data but received nothing',
                              code=StatusCode.BAD_REQUEST)
    return True