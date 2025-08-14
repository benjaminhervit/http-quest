from flask import request

import app.blueprints.quests.quest_factory as Q_factory
from app.blueprints.quests import bp
from app.request_handler import RequestHandler
from app.blueprints.quests.start.handlers import get_handlers_map

@bp.route("/start", methods=['GET'])
@bp.route("/start" + '/<username>', methods=['GET'])
def start(username=None):
    handlers = get_handlers_map()
    quest = Q_factory.get_start_quest()
    valid_methods = ['GET']
    response = RequestHandler.execute(request, quest, handlers, valid_methods)
    return response
