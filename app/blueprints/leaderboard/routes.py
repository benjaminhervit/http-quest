from flask import render_template

from app.blueprints.leaderboard import bp
from app.models import User


@bp.route("/", methods=["GET"])
def leaderboard():
    users = User.get_all()
    return render_template('leaderboard.html', data=users)
