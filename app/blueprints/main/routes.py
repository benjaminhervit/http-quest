from flask import render_template
from sqlalchemy.exc import OperationalError

from app.blueprints.main import bp
from app.models.user import User
from app. extensions import db


@bp.route("/")
def index():
    users = User.get_all()
    # try:
    #     users = User.get_all()
    # except OperationalError:
    #     db.create_all()
    #     users = []
    return render_template("index.html", users=users)
