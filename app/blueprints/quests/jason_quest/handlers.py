from flask import Request

from app.quest import QuestData
from app.authentication_manager import authenticator
from app.utils import content_generator, parser_utils

from app.errors import QuestError
from app.enums import QuestState, QuestTitle
from app.models import User


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.JASON_QUEST.value)

    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)

    formatting = {"HERO": username}
    content = content_generator.create_content(quest, state, formatting)
    return content


def post_handler(quest: QuestData, req: Request):
    # auth/get user
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.JASON_QUEST.value)

    # check state
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)
    
    # check json is set as content-type
    if not req.content_type:
        raise QuestError("Ufff... Like... I THINK there is a Jason in front of me but how can I know if I cannot look into his HEAD(ers) and see what TYPE he is? Try again.")
    
    if req.content_type != "application/json":
        raise QuestError(f"It may look like a Jason but when I look in its HEAD(ers) it says that it is a {req.content_type}? I'm not listening to this thing until it tells me that it is a Jason.")
    
    # check that json content is correct
    json = parser_utils.get_json(req)
    jason_you_are = json.get("jason_you_are", None)
    if not jason_you_are or jason_you_are != "hired":
        raise QuestError(f"Hm... I don't see that you have hired this Jason yet? All i see is: {json}. Read the quest instructions carefully again. Maybe check up on how to speak Json?")
    
    now = json.get("now", None)
    if not now or now != "march ahead!":
        raise QuestError(f"Okay, okay. You hired Jason alright but - what about NOW? This is what I got: {json} See the quest instructions.")
    
    # QUEST COMPLETED
    state = QuestState.COMPLETED.value
    User.update_xp(username, quest.xp)  # this one deserves a few extra points
    User.update_quest_state(username, QuestTitle.JASON_QUEST.value, state)  # complete this quest
    User.update_quest_state(username, QuestTitle.WALL_QUEST.value, QuestState.UNLOCKED.value)  # complete this quest
    
    formatting = content_generator.get_base_formatting()
    content = content_generator.create_content(quest, state, formatting)
    return content
