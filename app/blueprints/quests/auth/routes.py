from flask import request

from app.blueprints.quests.auth import bp
from app.request_manager import QuestRequestHandler
from app.authentication_manager import no_authentication
from .handlers import get_handlers
from .data import get_quest


@bp.route("/register", methods=["GET", "POST"])
def register():
    quest = get_quest()
    handlers = get_handlers()
    return QuestRequestHandler.execute(
        req=request,
        quest=quest,
        authenticator=no_authentication,
        handlers_map=handlers,
        html_template="register.html",
    )
