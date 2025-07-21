from app.enums import ParserKey

class Validator:
    
    def validate(self, parsed: dict, allowed_methods: list[str],
                 username_loc=None,
                 input_loc=None,
                 token_loc=None,
                 auth_type=None,
                 query_keys=None,
                 form_keys=None,
                 json_keys=None,
                 headers_keys=None):
        
        if parsed.get(ParserKey.METHOD) not in allowed_methods:
            return False
        
        if username_loc and parsed.get(username_loc) is None:
            return False
        
        if token_loc and parsed.get(token_loc) is None: 
            return False
        
        if input_loc and parsed.get(input_loc) is None: 
            return False
        
        if query_keys and self.keys_found_in_loc(parsed, query_keys,
                                                 ParserKey.QUERY_DATA):
            return False
        
        if form_keys and self.keys_found_in_loc(parsed, form_keys,
                                                ParserKey.FORM_DATA):
            return False
        
        if json_keys and self.keys_found_in_loc(parsed, json_keys,
                                                ParserKey.JSON_DATA):
            return False
        
        if headers_keys and self.keys_found_in_loc(
            parsed, headers_keys,
            ParserKey.HEADERS_DATA):
            
            return False
        
        # TODO: AUTH TYPE AND INPUT VALIDATION
        
            
    def keys_found_in_loc(self, parsed: dict, keys: list[str], loc: ParserKey):
        data: dict | None = parsed.get(loc)
        if data is None or data == {}:
            return False
        
        for key in keys:
            if data.get(key) is None:
                return False
        
        return True