from flask import Blueprint

bp = Blueprint('game', __name__, url_prefix='/game')

from app.blueprints.quests import routes
from app.blueprints.quests.start import start_route