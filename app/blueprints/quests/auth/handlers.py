from flask import Request

from app.extensions import db
from app.models import User
from app.enums import StatusCode, QuestState, QuestTitle
from app.errors import ParsingError, ValidationError, GameError
from app.utils import content_generator, parser_utils
from app.quest import QuestData


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    return content_generator.create_content(quest, QuestState.UNLOCKED.value)


def post_handler(quest: QuestData, req: Request):
    username = parser_utils.get_field_from_request_data(
        req, "username", parser_utils.get_form
    )
    if not username:
        raise GameError("Found no username in form?", StatusCode.BAD_REQUEST.value)
    if User.user_exists(username):
        raise ValidationError("Username already exists", StatusCode.BAD_REQUEST.value)
    #  add new user
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    
    # update user xp for succesfully registering
    User.update_xp(new_user, 1)
    #  complete start and register quest now that the user is registered
    User.update_quest_state(new_user, QuestTitle.START_QUEST.value,
                            QuestState.COMPLETED.value)
    User.update_quest_state(new_user, QuestTitle.REGISTER_QUEST.value,
                            QuestState.COMPLETED.value)
    # unlock the next quest
    User.update_quest_state(new_user, QuestTitle.IDENTIFY_QUEST.value,
                            QuestState.UNLOCKED.value)

    # build response content
    formatting = {"HERO": username}
    return content_generator.create_content(
        quest=quest, quest_state=QuestState.COMPLETED.value, formatting=formatting
    )
