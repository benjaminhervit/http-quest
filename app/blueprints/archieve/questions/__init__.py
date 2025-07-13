from flask import Blueprint

bp = Blueprint('questions', __name__, url_prefix='/questions')

from app.blueprints.questions import routes