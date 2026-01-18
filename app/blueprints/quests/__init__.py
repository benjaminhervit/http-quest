from flask import Blueprint

bp = Blueprint("game", __name__, url_prefix="/game")

from app.blueprints.quests import routes
from .start import routes
from .identify_yourself import routes
from .jason_quest import routes
from .delete_wall_quest import routes
from .repeat_quest import routes
from app.blueprints.manual import routes

from .get_all_quests import get_all_quests
