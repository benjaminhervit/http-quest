from flask import render_template
from sqlalchemy.exc import OperationalError

from app.blueprints.main import bp
from app.models import User, UserQuestState
from app.extensions import db


@bp.route("/")
def index():
    users = User.get_all()
    states = UserQuestState.get_all()
    data: list = []
    i = 0
    for u in users:
        data.append({'username':u.username})
        data[i]['states'] = [s.state for s in states if s.username == u.username]
        i += 1
    return render_template("index.html", data=data)
