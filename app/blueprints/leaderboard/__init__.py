from flask import Blueprint

bp = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")

from . import routes
