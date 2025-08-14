from flask import request

import app.blueprints.quests.quest_factory as Q_factory
from app.blueprints.quests.identify_yourself.handlers import get_handlers
from app.request_manager import RequestHandler
from app.blueprints.quests import bp

@bp.route('/identify-yourself', methods=['GET', 'POST'])
def register():
    quest = Q_factory.get_identify_yourself_quest()
    handlers = get_handlers()
    valid_methods = ['GET', 'POST']
    return RequestHandler.execute(request, quest, handlers, valid_methods)