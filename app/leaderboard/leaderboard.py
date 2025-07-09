from flask import Blueprint, render_template, request, url_for

from ..auth.auth import RegisterForm
from ..user_db.user_db import UserDatabase
from ..database import get_db

leaderboard_bp = Blueprint('/', __name__, template_folder='templates', static_folder='../../static')

@leaderboard_bp.route('/')
@leaderboard_bp.route('/home')
@leaderboard_bp.route('/index')
@leaderboard_bp.route('/leaderboard')
def index(username="", new_party=False, registration_message=""):
    form = RegisterForm()
    username = request.args.get('username', "")
    registration_message = request.args.get('registration_message', "")
    new_party = request.args.get('new_party', False)
    
    # Use the shared database access function
    db = get_db()
    teams = db.get_all_users()
    
    data = None
    
    # if new_party:
    #     level:Level = LB.createRegisterLevel()
    #     next_level:Level = LB.createTheTestLevel()
    #     data = level.get_victory_info(username, next_level.directions)

    return render_template('leaderboard/home.html', game_data=data, new_party = new_party, reg_msg = registration_message, form = form, teams=teams)