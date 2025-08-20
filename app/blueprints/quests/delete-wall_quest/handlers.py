
from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.authentication_manager import authenticator
from app.enums import QuestState


def get_handlers():
    return {
        'GET': get_handler,
        'POST': post_handler
    }


def get_handler(quest: QuestData, req: Request):
    state = QuestState.LOCKED.value
    formatting = content_generator.get_base_formatting()
    return "get handler template"


def post_handler(quest: QuestData, req: Request):
    state = QuestState.LOCKED.value
    formatting = content_generator.get_base_formatting()
    return "post_handler template"
