from flask import Blueprint

bp = Blueprint('game', __name__, url_prefix='/game')

from app.blueprints.quests import routes
from app.blueprints.quests.start import routes
from app.blueprints.quests.hire_jason import routes
from app.blueprints.quests.identify_yourself import routes