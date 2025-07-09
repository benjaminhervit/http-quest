from flask import render_template

from app.main import bp
from app.extensions import db
from app.models.user import User

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)