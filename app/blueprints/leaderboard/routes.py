from flask import render_template

from app.blueprints.leaderboard import bp
from app.models import User
import app.services as app_services

@bp.route("/", methods=["GET"])
def leaderboard():
    return render_template('leaderboard.html', data=app_services.get_leaderboard())
