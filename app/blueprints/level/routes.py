from app.blueprints.level import bp

@bp.route('/welcome')
def welcome():
    return "welcome to the game!"