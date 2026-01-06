from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.authentication_manager import authenticator
from app.enums import QuestState, QuestTitle
from app.models import User


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    return content_generator.create_content(quest, QuestState.UNLOCKED.value)


def post_handler(quest: QuestData, req: Request):
    #  Handle POST
    #  setup session
    username = parser_utils.get_auth_username(req)
    formatting = {"HERO": username or "Unknown Mysterious Savior"}
    state = User.get_user_quest_State(username, QuestTitle.IDENTIFY_QUEST.value)

    # check is quest is available
    if state == QuestState.UNLOCKED.value:
        state = QuestState.FAILED.value
        
        # check if authentication is correct
        if authenticator.authenticate_with_username(req):
            state = QuestState.COMPLETED.value
            User.update_xp(username, 1)
            
        # update quest state
        User.update_quest_state(username, QuestTitle.IDENTIFY_QUEST.value, state)
        
    # generate user response
    content = content_generator.create_content(quest, state, formatting)
    return content
