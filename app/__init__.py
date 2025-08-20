import os
from flask import Flask, current_app, request, g
from flask.cli import with_appcontext
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
    
    @app.before_request
    def _capture_request_snapshot():
        username = try_authenticate(request) or "dev"
        # print(f"user: {username}",
        #       f"endpoint: {request.endpoint}")
        if not username or request.endpoint in {"static", "api.get_all_users", "renderer.render_last_request"}:
            g._skip_reqlog = True
            return
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
            # print(f"req: {req_snap}\n\n")
            
            resp_snap = snapshot_response(resp, include_body=True)
            # print(f"resp: {resp_snap}")
            
            # print(f"route: {request.endpoint or request.path}",
            #       f"user: {username}",
            #       f"req_json: {json.dumps(req_snap)}",
            #       f"resp_json: {json.dumps(resp_snap)}")
            entry = LastUserRequestLog(
                route = request.endpoint or request.path,
                username = username,
                request_json = json.dumps(req_snap),
                response_json = json.dumps(resp_snap)
            )
            print(entry.username)
            
            db.session.add(entry)
            db.session.commit()
            
            latest = LastUserRequestLog.query.filter_by(username=username).first()
            #log_count = LastUserRequestLog.query.count()
            #print(f"Total LastUserRequestLog entries: {log_count}")
        except Exception:
            db.session.rollback()
            current_app.logger.exception("Request logging failed")
        return resp
        

    # Blueprints
    for bp in get_all_blueprints():
        app.register_blueprint(bp)

    # Create tables (and small seed) each time the serving process starts.
    # With in-memory SQLite this is required; with file DB this still works.
    with app.app_context():
        from app.models import listeners
        from app.models import User, Quest, UserQuestState, LastUserRequestLog
        
        # Only the serving process (child) should do this when reloader is on
        is_serving_proc = os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug
        
        print("DEBUG flags:",
              "AUTO_CREATE_DB =", app.config.get("AUTO_CREATE_DB"),
              "AUTO_SEED =", app.config.get("AUTO_SEED"),
              "app.debug =", app.debug,
              "WERKZEUG_RUN_MAIN =", os.environ.get("WERKZEUG_RUN_MAIN"))
        if app.config.get("AUTO_CREATE_DB") and is_serving_proc:
            print("I AM READY TO CREATE DB!")
            # Import models before create_all
            db.create_all()
            
            rows = [{"title": q.title, "xp": q.xp} for q in get_all_quests()]
            if rows:
                statement = sqlite_insert(Quest).values(rows)
                statement = statement.on_conflict_do_nothing(index_elements=["title"])
                db.session.execute(statement)
                db.session.commit()
            

            if app.config.get("AUTO_SEED") and not User.query.first():
                db.session.add(User(username="dev"))
                db.session.commit()

    return app
