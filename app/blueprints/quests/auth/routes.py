from flask import request

from app.blueprints.quests.auth import bp
import app.blueprints.quests.quest_factory as Q_factory
from app.blueprints.quests.auth.handlers import get_handlers
from app.request_manager import RequestHandler

@bp.route('/register', methods=['GET', 'POST'])
def register():
    quest = Q_factory.get_signup_quest()
    handlers = get_handlers()
    valid_methods = ['GET', 'POST']
    return RequestHandler.execute(request, quest, handlers,
                                  valid_methods, html_template='register.html')
