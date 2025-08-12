from flask import Blueprint

bp = Blueprint('renderer', __name__, url_prefix='/renderer')

from app.blueprints.quest_render import routes
