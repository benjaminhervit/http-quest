from flask import render_template

from app.blueprints.main import bp
from app.models.user import User

@bp.route('/')
def index():
    users = User.get_all()
    return render_template('index.html', users=users)