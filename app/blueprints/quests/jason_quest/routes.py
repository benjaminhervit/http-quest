
from flask import request

from .data import get_quest
from .handlers import get_handlers

from app.blueprints.quests import bp
from app.request_manager import RequestHandler

@bp.route("/hire-jason", methods=['GET', 'POST'])
def jason_route():
    handlers = get_handlers()
    quest = get_quest()
    valid_methods = ['GET', 'POST']
    response = RequestHandler.execute(request, quest, handlers, valid_methods)
    return response
