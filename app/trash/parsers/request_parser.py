from flask import Request
from app.errors import ParsingError
from app.enums import StatusCode, ParserKey
from app.models.quest import Quest

class RequestParser:
    @staticmethod
    def parse_method(req: Request):
        return req.method
    
    @staticmethod
    def parse_query(req: Request):
        return req.args.to_dict() if req.args else {}
    
    @staticmethod
    def parse_json(req: Request):
        return req.get_json(force=True, silent=True)
    
    
    @staticmethod
    def parse_path(req: Request):
        path: list[str] = req.path.split('/')
        return [p.strip() for p in path if p]
    
    @staticmethod
    def parse_form(req: Request):
        if req.method == 'POST':
            return req.form.to_dict() if req.form else {}
        return {}
    
    @staticmethod
    def parse(req: Request):
        try:
            return {
                ParserKey.METHOD_DATA: RequestParser.parse_method(req),
                ParserKey.PATH_DATA: RequestParser.parse_path(req),
                ParserKey.QUERY_DATA: RequestParser.parse_query(req),
                ParserKey.FORM_DATA: RequestParser.parse_form(req)
            }
        except ParsingError as exc:
            raise ParsingError(f'Failed to parse request: {req} - {str(exc)}',
                               StatusCode.BAD_REQUEST.value) from exc