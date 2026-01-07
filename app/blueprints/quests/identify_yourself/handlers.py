from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.authentication_manager import authenticator
from app.enums import QuestState, QuestTitle
from app.models import User
from app.errors import ParsingError


def get_handlers():
    return {"GET": get_handler}


def get_handler(quest: QuestData, req: Request):
    try:
        # run this if the quest is accessed with authorization 
        username = parser_utils.get_auth_username(req)
        state = User.get_user_quest_State(username, QuestTitle.IDENTIFY_QUEST.value)
        
        # check if authentication is correct
        if authenticator.authenticate_with_username(req):
            state = QuestState.COMPLETED.value
            User.update_xp(username, 1)
            
        # update quest state
        User.update_quest_state(username, QuestTitle.IDENTIFY_QUEST.value, state)
        # unlock next quest
        User.update_quest_state(username, QuestTitle.JASON_QUEST.value, QuestState.UNLOCKED.value)
            
        # generate user response
        formatting = {"HERO": username or "Unknown Mysterious Savior"}
        content = content_generator.create_content(quest, state, formatting)
        return content
    except ParsingError:
        # default response if there is no authorization
        content = content_generator.create_content(quest, QuestState.UNLOCKED.value)
        return content