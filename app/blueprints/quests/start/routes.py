from flask import request

from app.blueprints.quests import bp
from app.request_manager import QuestRequestHandler
from app.authentication_manager import no_authentication

from .handlers import get_handlers
from .data import get_start_quest


@bp.route("/start", methods=["GET"])
@bp.route("/start" + "/<username>", methods=["GET"])
def start(username=None):
    handlers = get_handlers()
    quest = get_start_quest()
    # valid_methods = ["GET"]
    response = QuestRequestHandler.execute(
        req=request,
        quest=quest,
        authenticator=no_authentication,
        handlers_map=handlers,
        # valid_req_methods=valid_methods,
    )
    return response
