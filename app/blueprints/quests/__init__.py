from flask import Blueprint

bp = Blueprint('game', __name__, url_prefix='/game')

from app.blueprints.quests import routes
from app.blueprints.quests.start import start_route
from app.blueprints.quests.hire_jason import hire_json_route