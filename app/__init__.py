from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

from app.config import Config, TestingConfig
import logging

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

logging.basicConfig(
    level=logging.DEBUG,  # or INFO, WARNING, ERROR
    format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'
)

blueprints = [main_bp, auth_bp, quest_bp, dash_bp]

def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.debug = True

    db.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route('/test')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app