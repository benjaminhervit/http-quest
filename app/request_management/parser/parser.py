from flask import Request
from app.errors import ParsingError
from app.enums import StatusCode, ParserKey
from app.models.quest import Quest

class Parser:
    def __init__(self, method_fn, path_fn, query_fn, json_fn, form_fn,
                 header_fn, username_fn, token_fn, input_fns) -> None:

        self.method_fn = method_fn
        self.path_fn = path_fn
        self.query_fn = query_fn
        self.json_fn = json_fn
        self.form_fn = form_fn
        self.header_fn = header_fn
        self.username_fn = username_fn
        self.token_fn = token_fn
        self.input_fns = input_fns
    
    def parse_request(self, req: Request):
        try:
            return {
                ParserKey.METHOD_DATA: self.method_fn(req=req),
                ParserKey.PATH_DATA: self.path_fn(req=req),
                ParserKey.QUERY_DATA: self.query_fn(req=req),
                ParserKey.JSON_DATA: self.json_fn(req=req),
                ParserKey.FORM_DATA: self.form_fn(req=req),
                ParserKey.HEADERS_DATA: self.header_fn(req=req),
                ParserKey.USERNAME: self.username_fn(req=req)
            }
        except ParsingError as exc:
            raise ParsingError(f'Failed to parse request: {req} - {str(exc)}',
                               StatusCode.BAD_REQUEST.value) from exc
    
    @staticmethod
    def parse_quest_settings(quest: Quest):
        try:
            return {
                ParserKey.ALLOWED_REQ_METHODS: [q.strip().upper() for q in quest.allowed_req_methods.split(',')],
                ParserKey.JSON_KEYS: quest.json_keys,
                ParserKey.QUERY_KEYS: quest.query_keys,
                ParserKey.FORM_KEYS: quest.form_keys,
                ParserKey.HEADERS_KEYS: quest.headers_keys,
                ParserKey.USERNAME_LOC: quest.username_loc,
                ParserKey.TOKEN_LOC: quest.token_loc,
                ParserKey.INPUT_LOC: quest.input_loc,
                ParserKey.AUTH_TYPE: quest.auth_type,
                ParserKey.ANSWER_KEY: quest.answer_key
            }
        except ParsingError as exc:
            raise ParsingError(f'Failed to parse quest settings: {quest}',
                               code=StatusCode.SERVER_ERROR.value) from exc
            
    def create_request_parser(settings:dict):
        import app.request_management.parser.request_strategies as strategies