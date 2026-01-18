from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.enums import QuestState, QuestTitle, ContentKeys
from app.models import User
from app.authentication_manager import authenticator
from app.errors import ParsingError


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.IDENTIFY_QUEST.value)
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)
    
    formatting = {"HERO": username}
    content = content_generator.create_content(quest, state, formatting)
    return content


def post_handler(quest: QuestData, req: Request):
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.IDENTIFY_QUEST.value)
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)
    
    jason_says = parser_utils.get_field_from_request_data(
        req, "say", parser_utils.get_json
    )
    
    if not jason_says.lower() == "please":
        raise ParsingError("... I am quite literal when I want jason to say:please")
    
    counter = User.increment_beg_counter(username)
    if counter < 3:
        formatting = {"HERO": username or "Unknown Mysterious Savior"}
        content = content_generator.create_content(quest, state, formatting)
        content.update({ContentKeys.STORY.value: f"YEEEES! That was {counter}. Just {3-counter} more to go!"})
        return content
    
    # COMPLETED!
    state = QuestState.COMPLETED.value
    User.update_quest_state(username, QuestTitle.BEG_QUEST.value, state)
    #User.update_quest_state(username, NEXT QUEST TO UNLOCK GOES HERE!, QuestState.UNLOCKED.value)
    
    # generate user response
    formatting = {"HERO": username or "Unknown Mysterious Savior"}
    content = content_generator.create_content(quest, state, formatting)
    return content
