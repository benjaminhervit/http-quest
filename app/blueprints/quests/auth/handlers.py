from flask import Request

from app.extensions import db
from app.models import User, UserQuestState
from app.enums import StatusCode, QuestState
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
        raise ParsingError("Found no username in form?", StatusCode.BAD_REQUEST.value)
    if User.user_exists(username):
        raise ValidationError("Username already exists", StatusCode.BAD_REQUEST.value)
    #  add new user
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    
    state_obj: UserQuestState | None = UserQuestState.get_state(username, quest.title)
    if not state_obj:
        raise GameError('Could not find state obj for user and quest'
                        f'user: {username}, quest: {quest.title}',
                        StatusCode.SERVER_ERROR.value)
    
    xp_awarded = UserQuestState.complete_and_award_xp(username, quest.title)
    print(f"GOT XP: {xp_awarded}")
    
    #  build response content
    formatting = {"HERO": username}
    return content_generator.create_content(
        quest=quest,
        quest_state=QuestState.COMPLETED.value,
        formatting=formatting)
