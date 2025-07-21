from flask import Blueprint

bp = Blueprint('data', __name__, url_prefix='/data')

from app.blueprints.dashboard import routes
