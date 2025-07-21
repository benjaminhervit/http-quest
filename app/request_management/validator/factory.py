from app.request_management.validator.validator import Validator
import app.request_management.validator.strategies as strategies
from app.enums import InputLocation, StatusCode
from app.errors import ValidationError

functions = {
    InputLocation.PATH_DATA: strategies.any_data_expected,
    InputLocation.QUERY_DATA: strategies.any_data_expected,
    InputLocation.NONE: strategies.none_method
}

def create_validator(content_loc: str, ) -> Validator:
    return Validator()
    # if content not in InputLocation:
    #     raise ValidationError(
    #         'content validation def identifier is not a not valid enum.',
    #         code=StatusCode.SERVER_ERROR)
    # if username not in InputLocation:
    #     raise ValidationError(
    #         'username validation def identifier is not a not valid enum',
    #         code=StatusCode.SERVER_ERROR)
    # if token not in InputLocation:
    #     raise ValidationError(
    #         'token validation def identifier is not a not valid enum',
    #         code=StatusCode.SERVER_ERROR)
    
    # content_fn = functions.get(InputLocation(content))
    # username_fn = functions.get(InputLocation(username))
    # token_fn = functions.get(InputLocation(token))
    
    # return Validator(content_fn=content_fn,
    #                  username_fn=username_fn,
    #                  token_fn=token_fn)