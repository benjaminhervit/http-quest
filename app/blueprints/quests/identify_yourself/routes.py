from flask import request

from app.request_manager import QuestRequestHandler
from app.blueprints.quests import bp
from app.authentication_manager import no_authentication
from .handlers import get_handlers
from .data import get_quest


@bp.route("/identify-yourself", methods=["GET", "POST"])
def register():
    quest = get_quest()
    handlers = get_handlers()
    return QuestRequestHandler.execute(
        req=request,
        quest=quest,
        authenticator=no_authentication,
        handlers_map=handlers,
    )
