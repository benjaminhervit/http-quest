import os
from flask import Flask, current_app
from flask.cli import with_appcontext

from .extensions import db
from .config import DevelopmentConfig

from app.blueprints import get_all_blueprints
from app.blueprints.quests import get_all_quests

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Extensions
    db.init_app(app)

    # Blueprints
    for bp in get_all_blueprints():
        app.register_blueprint(bp)

    # Create tables (and small seed) each time the serving process starts.
    # With in-memory SQLite this is required; with file DB this still works.
    with app.app_context():
        from app.models import listeners
        
        # Only the serving process (child) should do this when reloader is on
        is_serving_proc = os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug

        if app.config.get("AUTO_CREATE_DB") and is_serving_proc:
            # Import models before create_all
            from app.models import User, Quest, UserQuestState  # noqa: F401
            db.create_all()
            
            for q in get_all_quests():
                db.session.add(Quest(title=q.title, xp=q.xp))
            db.session.commit()
            

            if app.config.get("AUTO_SEED") and not User.query.first():
                from app.models import User
                db.session.add(User(username="dev"))
                db.session.commit()

    return app
