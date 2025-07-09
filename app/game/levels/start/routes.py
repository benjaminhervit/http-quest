from app.game.levels.start import bp

@bp.route('/welcome/<string:username>')
def welcome(username):
    if username is None:
        return "<h1> You are missing a level "