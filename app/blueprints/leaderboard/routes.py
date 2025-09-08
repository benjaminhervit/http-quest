from flask import render_template

from app.blueprints.leaderboard import bp
from app.models import User, UserQuestState


@bp.route("/", methods=["GET"])
def leaderboard():
    users = User.get_all()
    states = UserQuestState.get_all()
    data: list = []
    i = 0
    for u in users:
        data.append({'username':u.username})
        data[i]['states'] = [s.state for s in states if s.username == u.username]
        i += 1
    print(data)
    return render_template('leaderboard.html', data=data)
