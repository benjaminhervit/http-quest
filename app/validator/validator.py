from app.enums import ParserKey, StatusCode, ReqMethodType
from app.errors import ValidationError

class Validator:
    
    @staticmethod
    def validate_request(parsed: dict, settings: dict):
        # method
        Validator.validate_method_data(parsed.get(ParserKey.METHOD_DATA),
                                       settings.get(ParserKey.METHOD_DATA))
        
        # query
        Validator.validate_query_data(settings.get(ParserKey.QUERY_KEYS),
                                      parsed.get(ParserKey.QUERY_DATA) or {})
        
        return True
    
    
    @staticmethod
    def validate_method_data(method: str | None, allowed: list[str] | None):
        
        if not isinstance(allowed, list):
            raise ValueError('Allowed methods should be list.')
        
        if method not in ReqMethodType:
            raise ValidationError(f'Could not recognize request method {method}',
                                  code=StatusCode.BAD_REQUEST)
        
        if method not in allowed:
            raise ValidationError(f'Use request method {method} is not valid.',
                                  code=StatusCode.BAD_REQUEST)
        
        return True
    
    
    @staticmethod
    def validate_json_data(keys: list[str] | None, data: dict):
        return Validator.check_for_key_data_match(keys, data, 'JSON')
    
    
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
            raise ValidationError(f'No keys but fount data in {loc}: {data}.')
        
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