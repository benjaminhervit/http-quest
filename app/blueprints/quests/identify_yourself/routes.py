from flask import request

from app.request_manager import RequestHandler
from app.blueprints.quests import bp
from .handlers import get_handlers
from .data import get_quest

@bp.route('/identify-yourself', methods=['GET', 'POST'])
def register():
    quest = get_quest()
    handlers = get_handlers()
    valid_methods = ['GET', 'POST']
    return RequestHandler.execute(request, quest, handlers, valid_methods)