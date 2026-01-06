from flask import render_template
from sqlalchemy.exc import OperationalError

from app.blueprints.main import bp
from app.models import User
from app.extensions import db
import app.services as app_services


@bp.route("/")
def index():
    return render_template("index.html", data=app_services.get_leaderboard())
