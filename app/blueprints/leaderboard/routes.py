from flask import render_template

from app.blueprints.leaderboard import bp


@bp.route("/", methods=["GET"])
def leaderboard():
    return render_template('leaderboard.html')
