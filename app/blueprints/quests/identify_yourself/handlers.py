from flask import Request

from app.quest import QuestData, QuestSession
from app.utils import content_generator, parser_utils
from app.authentication_manager import authenticator
from app.enums import QuestState
from app.models import UserQuestState


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    return content_generator.create_start_content(quest)


def post_handler(quest: QuestData, req: Request):
    #  Handle POST
    #  setup session
    username = parser_utils.get_auth_username(req)
    formatting = {"HERO": username or "Unknown Mysterious Savior"}
    session = QuestSession(quest.title, username)
    
    if session.state != QuestState.UNLOCKED.value:
        return content_generator.create_content(quest, session.state, formatting)
    
    session.state = QuestState.FAILED.value
    if authenticator.authenticate(req):
        session.state = QuestState.COMPLETED.value
        UserQuestState.complete_and_award_xp(session.username, session.quest_title)
    return content_generator.create_content(quest, session.state, formatting)
    
