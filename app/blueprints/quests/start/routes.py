from flask import request

from app.blueprints.quests import bp
from app.request_manager import RequestHandler

from .handlers import get_handlers
from .data import get_start_quest


@bp.route("/start", methods=["GET"])
@bp.route("/start" + "/<username>", methods=["GET"])
def start(username=None):
    handlers = get_handlers()
    quest = get_start_quest()
    valid_methods = ["GET"]
    response = RequestHandler.execute(request, quest, handlers, valid_methods)
    return response
