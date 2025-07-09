from flask import render_template, request

from app.blueprints.main import bp
from app.models.user import User

@bp.route('/')
def index():
    new_user = request.args.get('new_user', False) #default for startup
    print(f"user: {new_user}")
    users = User.query.all()
    return render_template('index.html', users=users, new_user=new_user)