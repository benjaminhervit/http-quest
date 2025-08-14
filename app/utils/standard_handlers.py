from flask import Request
from app.quest import QuestData
from app.utils import parser_utils, content_generator
from app.authentication_manager import authenticator

def standard_get_handler(quest: QuestData, req: Request):
    username = parser_utils.get_auth_username(req)
    if authenticator.authenticate(req):
        content = content_generator.create_start_content(quest)
        placeholders = {'[HERO]': username}
        content = content_generator.replace_placeholders(content, placeholders)
        return content
    return "something went wrong. You should not end up here?"