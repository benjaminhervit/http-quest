from flask import Request
from app.errors import ParsingError
from app.enums import StatusCode, ParserKey
from app.models.quest import Quest

class Parser:
    
    
    @staticmethod
    def parse_json(req: Request):
        return req.get_json(force=True, silent=True)
    
    
    @staticmethod
    def parse_query(req: Request):
        return req.args.to_dict() if req.args else {}
    
    
    @staticmethod
    def parse_method(req: Request):
        return req.method
    
    
    @staticmethod
    def parse_path(req: Request):
        path: list[str] = req.path.split('/')
        return [p.strip() for p in path if p]
    
    @staticmethod
    def parse_request(req: Request):
        try:
            return {
                ParserKey.METHOD_DATA: Parser.parse_method(req),
                ParserKey.PATH_DATA: Parser.parse_path(req),
                ParserKey.QUERY_DATA: Parser.parse_query(req),
            }
        except ParsingError as exc:
            raise ParsingError(f'Failed to parse request: {req} - {str(exc)}',
                               StatusCode.BAD_REQUEST.value) from exc
    
    
    @staticmethod
    def parse_quest_settings(quest: Quest):
        try:
            return {
                ParserKey.METHOD_DATA: Parser.get_keys_list(
                    quest.allowed_req_methods) if quest.allowed_req_methods
                else [],
                
                ParserKey.JSON_KEYS: Parser.get_keys_list(
                    quest.json_keys) if quest.json_keys
                else [],
                
                ParserKey.QUERY_KEYS: Parser.get_keys_list(
                    quest.query_keys) if quest.query_keys
                else [],

                ParserKey.FORM_KEYS: Parser.get_keys_list(
                    quest.form_keys) if quest.form_keys
                else [],
                
                ParserKey.HEADERS_KEYS: Parser.get_keys_list(
                    quest.headers_keys) if quest.headers_keys
                else [],
                
                ParserKey.USERNAME_LOC: quest.username_loc,
                ParserKey.TOKEN_LOC: quest.token_loc,
                ParserKey.INPUT_LOC: quest.input_loc,
                ParserKey.AUTH_TYPE: quest.auth_type,
                ParserKey.ANSWER_KEY: quest.answer_key
            }
        except ParsingError as exc:
            raise ParsingError(f'Failed to parse quest settings: {quest}',
                               code=StatusCode.SERVER_ERROR.value) from exc
    
    @staticmethod
    def get_keys_list(string: str):
        return [q.strip() for q in string.split(',')]
    
    @staticmethod
    def get_filtered_parse(parsed: dict, settings: dict):
        look_up = {
            ParserKey.METHOD_DATA: ParserKey.METHOD_DATA,
            ParserKey.QUERY_KEYS: ParserKey.QUERY_DATA,
            ParserKey.FORM_KEYS: ParserKey.FORM_DATA,
            ParserKey.JSON_KEYS: ParserKey.JSON_DATA,
            ParserKey.HEADERS_KEYS: ParserKey.HEADERS_DATA
        }

        result = {}
        for k, v in settings.items():
            if v:
                result[look_up[k]] = parsed[look_up[k]]
        return result