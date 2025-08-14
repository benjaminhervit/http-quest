from flask import request

from app.blueprints.quests.auth import bp
from app.request_manager import RequestHandler
from .handlers import get_handlers
from .data import get_quest


@bp.route("/register", methods=["GET", "POST"])
def register():
    quest = get_quest()
    handlers = get_handlers()
    valid_methods = ["GET", "POST"]
    return RequestHandler.execute(
        request, quest, handlers, valid_methods, html_template="register.html"
    )
