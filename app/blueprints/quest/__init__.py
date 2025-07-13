from flask import Blueprint



bp = Blueprint('level', __name__, url_prefix='/level')

from app.blueprints.quest import routes