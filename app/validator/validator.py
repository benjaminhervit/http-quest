from app.enums import ParserKey, QuestKey, StatusCode, ReqMethodType
from app.errors import ValidationError
from app.utils import get_enum_values_as_list

class Validator:
    
    @staticmethod
    def validate_request(parsed: dict, settings: dict):
        # validate settings keys
        Validator.validate_input_keys(list(settings.keys()),
                                      get_enum_values_as_list(QuestKey))
        
        # validate parsed input keys
        Validator.validate_input_keys(list(parsed.keys()),
                                      get_enum_values_as_list(ParserKey))
        
        # method
        Validator.validate_req_method(parsed.get(ParserKey.METHOD_DATA),
                                      settings.get(QuestKey.METHOD_DATA) or [])
        
        # query
        Validator.validate_query_data(settings.get(QuestKey.QUERY_KEYS) or [],
                                      parsed.get(ParserKey.QUERY_DATA) or {})
        
        return True
    
    
    @staticmethod
    def validate_req_method(method: str | None, allowed: list[str]):
        
        if not isinstance(allowed, list):
            raise ValueError('Allowed methods should be list.')
        
        if method not in get_enum_values_as_list(ReqMethodType):
            raise ValidationError(f'Could not recognize request method {method}',
                                  code=StatusCode.BAD_REQUEST)
        
        if method not in allowed:
            raise ValidationError(f'Use request method {method} is not valid.',
                                  code=StatusCode.BAD_REQUEST)
        
        return True
    
    
    @staticmethod
    def validate_query_data(keys: list[str] | None, data: dict):
        return Validator.check_for_key_data_match(keys, data, 'Query')
    
        
    @staticmethod
    def check_for_key_data_match(keys: list[str] | None,
                                 data: dict, loc: str):
        
        if not isinstance(keys, list):
            raise TypeError(f'Expected keys to be list[str] in {loc}.')
            
        if not isinstance(data, dict):
            raise TypeError(f'Expected data to be dict in {loc}.')
        
        if not keys and data:
            raise ValidationError(f'No keys but fount data in {loc}: {data}.'
                                  ' Do not send data in the wrong places.')
        
        if keys and not data:
            raise ValidationError(f'Found keys: {keys} but not data in {loc}.')
        
        if len(keys) > len(data.keys()) or len(keys) < len(data.keys()):
            raise ValidationError(f'Expected {len(keys)} keys: {keys} in'
                                  f' {loc} but got '
                                  f'{len(data.keys())} keys: {data.keys()}')
        
        if not set(keys).issubset(data.keys()):
            raise ValidationError(f'Could not find key {keys} in {loc}:'
                                  f' {data} - {list(data.keys())}')

        return True
    
    @staticmethod
    def validate_input_keys(input_keys: list, allowed_keys: list) -> bool:
        if not set(input_keys).issubset(set(allowed_keys)):
            raise ValueError(
                f'Found one or more setting keys that are not valid.\n '
                f'settings keys: {input_keys},\n '
                f'allowed keys: {allowed_keys}'
            )
        return True
