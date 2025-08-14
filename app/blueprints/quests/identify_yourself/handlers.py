from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.authentication_manager import authenticator


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    return content_generator.create_start_content(quest)


def post_handler(quest: QuestData, req: Request):
    #  Handle POST
    username = parser_utils.get_auth_username(req)
    if authenticator.authenticate(req):
        #  build response content
        formatting = {"HERO": username}
        content = content_generator.create_completed_content(quest, formatting)
        return content
