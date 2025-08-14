from flask import Blueprint

bp = Blueprint('game', __name__, url_prefix='/game')

from app.blueprints.quests import routes
from .start import routes
from .identify_yourself import routes
from .jason_quest import routes