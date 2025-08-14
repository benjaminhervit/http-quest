
from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils, standard_get_handler
from app.authentication_manager import authenticator

def get_handlers():
    return {
        'GET': get_handler,
        'POST': post_handler
    }


def get_handler(quest: QuestData, req: Request):
    return standard_get_handler(req=req, quest=quest)


def post_handler(quest: QuestData, req: Request):
    if authenticator.authenticate(req):
        hire_jason = parser_utils.get_field_from_request_data(
            req,
            'jason',
            parser_utils.get_json)

        if hire_jason == 'hire':
            username = parser_utils.get_auth_username(req)
            formatting = {'HERO': username}
            return content_generator.create_completed_content(quest, formatting)
        
    return "you should not get this far"
