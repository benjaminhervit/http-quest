
from flask import Request

from app.utils import send_response

from app.enums import StatusCode
from app.errors import ParsingError, ValidationError, GameError
from app.utils import content_generator
from app.quest import QuestData


class RequestHandler:
    
    @classmethod
    def validate_handlers_map(cls, handlers_map: dict,
                              valid_methods: list) -> bool:
        
        for m in valid_methods:
            if m not in handlers_map:
                raise ValueError(f'Missing handler for method {m}')
        return True
                
    
    @classmethod
    def execute(cls, req: Request, quest: QuestData,
                handlers_map: dict, valid_req_methods: list,
                html_template: str = 'quest_renderer.html'):
        
        #validate
        cls.validate_handlers_map(handlers_map, valid_req_methods)
        
        try:
            #  Setup
            content = content_generator.create_locked_content(quest)
            handler = handlers_map.get(req.method)
            if not handler:
                raise GameError(f'Could not find handler for method'
                                f'{req.method}',
                                StatusCode.SERVER_ERROR.value)
            content = handler(quest=quest, req=req)
            
            return send_response(req, content, StatusCode.OK.value,
                                 html_template)

        # error handling
        except ParsingError as e:
            content = content_generator.create_error_msg(str(e),
                                                         'ParsingError',
                                                         e.code)
            return send_response(req, content, StatusCode.SERVER_ERROR.value,
                                 html='error_message.html')

        except ValidationError as e:
            content = content_generator.create_error_msg(str(e),
                                                         'ValidationError',
                                                         e.code)
            return send_response(req, content, e.code,
                                 html='error_message.html')

        except GameError as e:
            content = content_generator.create_error_msg(str(e),
                                                         'GameError', e.code)
            return send_response(req, content, e.code,
                                 html='error_message.html')