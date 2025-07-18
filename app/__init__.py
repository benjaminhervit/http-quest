from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 

from config import Config

#import db
from app.extensions import db

#blueprints
from app.blueprints.main import bp as main_bp
from app.blueprints.auth import bp as auth_bp
from app.blueprints.quest import bp as quest_bp
blueprints = [main_bp, auth_bp, quest_bp]

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.debug = True
    
    #init db
    db.init_app(app)
    
    with app.app_context():
        db.drop_all()     # ❗ DANGER: drops all tables
        db.create_all()   # recreates them fresh
    
    # Register blueprint
    for bp in blueprints:
        app.register_blueprint(bp)
    
    @app.route('/test')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    return app