from flask import Flask, current_app, request, g
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
import json

from .extensions import db
from .config import DevelopmentConfig

from .blueprints import get_all_blueprints
from .blueprints.quests import get_all_quests

from .authentication_manager import try_authenticate
from .utils import snapshot_response, snapshot_request

from .models import LastUserRequestLog


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Extensions
    db.init_app(app)

    # Blueprints
    for bp in get_all_blueprints():
        app.register_blueprint(bp)

    @app.before_request
    def _capture_request_snapshot():
        username = try_authenticate(request)
        is_quest: bool = (request.endpoint or request.path).__contains__("game")

        if not username or is_quest is False:
            g._skip_reqlog = True
            return
        print("New log ordered in before_request")
        g._current_user = username
        g._req_snapshot = snapshot_request(request, username, include_body=True)

    @app.after_request
    def _capture_response_snapshot(resp):
        try:
            if getattr(g, "_skip_reqlog", False):
                return resp

            req_snap = getattr(g, "_req_snapshot", None)
            username = getattr(g, "_current_user", "dev")
            if req_snap is None:
                req_snap = snapshot_request(request, username, include_body=False)

            resp_snap = snapshot_response(resp, include_body=True)

            log: LastUserRequestLog | None = LastUserRequestLog.upsert_for_username(
                username=username,
                route=request.endpoint or request.path,
                request_json=json.dumps(req_snap),
                response_json=json.dumps(resp_snap),
            )
            print(f"Log created for user {username}") if log else print("No new log")

        except Exception:
            db.session.rollback()
            current_app.logger.exception("Request logging failed")
        return resp
    
    @app.teardown_appcontext
    def close_connection(_exception):
        """Close the database, when Flask exits.

        Args:
            _exception (_type_): not used   
        """
        db_instance = getattr(g, '_database', None)
        if db_instance is not None:
            db_instance.close()

    # Create tables (and small seed) each time the serving process starts.
    with app.app_context():
        from app.models import User, LastUserRequestLog

        db.create_all()

        if app.config.get("AUTO_SEED") and not User.query.first():
            db.session.add(User(username="dev"))
            db.session.commit()

    return app
