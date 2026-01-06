from flask import render_template
from sqlalchemy.exc import OperationalError

from app.blueprints.main import bp
from app.models import User
from app.extensions import db


@bp.route("/")
def index():
    users = User.get_all()
    return render_template("index.html", data=users)
