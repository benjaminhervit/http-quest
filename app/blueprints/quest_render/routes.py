from flask import render_template, session, jsonify, request
import json
from app.blueprints.quest_render import bp
from app.errors import ParsingError, AuthenticationError
from app.enums import StatusCode
from app.models import LastUserRequestLog
from app.utils import parser_utils


@bp.route("/", methods=["GET"])
def renderer():
    content = session.pop("content", None)
    print(content)
    return render_template("quest_renderer.html", content=content)

@bp.route("/last-request", methods=["GET"])
def render_last_request():
    try:
        content: LastUserRequestLog | None = LastUserRequestLog.query.first()
        
        user: str | None = parser_utils.get_field_from_request_data(request, 'username', parser_utils.get_query)
        print(f"USER: {user}")
        if user:
            content: LastUserRequestLog | None = LastUserRequestLog.query.filter_by(username=user).first()
        
        if not isinstance(content, LastUserRequestLog):
            return ParsingError('Could not parse last request',
                                StatusCode.SERVER_ERROR.value)
        data = content.to_dict()
        req = data.get("request_json", "")
        data.update({"request_json": json.loads(req) if req else ""})
        
        resp = data.get("response_json", "")
        resp_json = json.loads(resp) if resp else None
        if resp_json:
            body = resp_json["body_text"] or None
            print(body)
            print(type(body))
            body_json = json.loads(body) if body else ""
            print(body_json)
            resp_json["body_text"] = body_json
        data.update({"response_json": resp_json if resp else ""})
    
        return render_template("logging.html", content=data)            
    
    except ParsingError as e:
        return (jsonify({'error': str(e)}),
                StatusCode.UNAUTHORIZED.value)
    except AuthenticationError as e:
        return (jsonify({'error': str(e)}),
                StatusCode.UNAUTHORIZED.value)