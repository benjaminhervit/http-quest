from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 

from config import Config

#import db
from app.extensions import db

#blueprints
from app.main import bp as main_bp
from app.posts import bp as posts_bp
from app.questions import bp as question_bp
from app.auth import bp as auth_bp
blueprints = [main_bp, posts_bp, question_bp, auth_bp]

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #init db
    db.init_app(app)
    
    # Register blueprint
    for bp in blueprints:
        app.register_blueprint(bp)
    
    @app.route('/test')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    return app