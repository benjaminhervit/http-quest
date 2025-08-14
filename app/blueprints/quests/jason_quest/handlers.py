
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
    #username = parser_utils.get_auth_username(req)
    #if authenticator.authenticate(req):
    #    pass
    return "get_handler template"
