from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

from config import Config

#import db
from app.extensions import db
from app.game.quests import quests

from app.game.quests.welcome import welcome_Q
from app.game.quests.accept import accept_Q

#blueprints
from app.blueprints.main import bp as main_bp
from app.blueprints.auth import bp as auth_bp
from app.blueprints.quest import bp as quest_bp
from app.blueprints.dashboard import bp as dash_bp
blueprints = [main_bp, auth_bp, quest_bp, dash_bp]

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.debug = True
    
    #init db
    db.init_app(app)
    
    from app.models.quest import Quest
    from app.models.user import User
    from app.models.user_quest_state import UserQuestState
    from app.models.listeners import populate_user_state_after_commit
    with app.app_context():
        db.drop_all()     # ❗ DANGER: drops all tables
        db.create_all()
        db.session.add_all(quests)
        db.session.commit()
        
        accept_Q.prev_quest_id = welcome_Q.id
        db.session.commit()
        
        db.session.add(User(username="test_user"))
        db.session.commit()
        
    
    # Register blueprint
    for bp in blueprints:
        app.register_blueprint(bp)
    
    @app.route('/test')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    return app