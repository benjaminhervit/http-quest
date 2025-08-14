from flask import Request

from app.extensions import db
from app.models.user import User
from app.enums import StatusCode
from app.errors import ParsingError, ValidationError
from app.utils import content_generator, parser_utils
from app.quest import QuestData


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    return content_generator.create_start_content(quest)


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

    #  build response content
    formatting = {"HERO": username}
    return content_generator.create_completed_content(quest, formatting)
