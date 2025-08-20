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
        if not content:
            return jsonify({'error': 'No logs created yet'})
        
        user: str | None = parser_utils.get_field_from_request_data(request, 'username', parser_utils.get_query)
        if user:
            content: LastUserRequestLog | None = LastUserRequestLog.query.filter_by(username=user).first()
        
        if not isinstance(content, LastUserRequestLog):
            return ParsingError('Could not parse last request',
                                StatusCode.SERVER_ERROR.value)
            
        # convert data strings to json
        data = content.to_dict()
        data["request_json"] = parser_utils.try_json_loads(data.get("request_json"), {})
        
        resp = parser_utils.try_json_loads(data.get("response_json"), {})
        resp["body_text"] = parser_utils.try_json_loads(resp.get("body_text"), {})
        data["response_json"] = resp
    
        return render_template("logging.html", content=data)            
    
    except ParsingError as e:
        return (jsonify({'error': str(e)}),
                StatusCode.UNAUTHORIZED.value)
    except AuthenticationError as e:
        return (jsonify({'error': str(e)}),
                StatusCode.UNAUTHORIZED.value)