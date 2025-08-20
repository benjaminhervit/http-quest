from flask import request

from .data import get_quest
from .handlers import get_handlers

from app.blueprints.quests import bp
from app.request_manager import QuestRequestHandler
from app.authentication_manager import authenticate_with_username


@bp.route("/hire-jason", methods=["GET", "POST"])
def jason_route():
    handlers = get_handlers()
    quest = get_quest()
    valid_methods = ["GET", "POST"]
    response = QuestRequestHandler.execute(
        req=request,
        quest=quest,
        authenticator=authenticate_with_username,
        handlers_map=handlers,
        valid_req_methods=valid_methods)
    return response
