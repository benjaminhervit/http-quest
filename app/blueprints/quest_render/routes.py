from flask import render_template, session, request, jsonify
from app.blueprints.quest_render import bp
from app.authentication_manager import authenticate_with_username
from app.utils import responder
from app.errors import ParsingError, AuthenticationError
from app.enums import StatusCode
from app.models import LastUserRequestLog


@bp.route("/", methods=["GET"])
def renderer():
    content = session.pop("content", None)
    print(content)
    return render_template("quest_renderer.html", content=content)

@bp.route("/last-request", methods=["GET"])
def render_last_request():
    try:
        content: LastUserRequestLog | None = LastUserRequestLog.query.first()
        if not isinstance(content, LastUserRequestLog):
            return ParsingError('Could not parse last request',
                                StatusCode.SERVER_ERROR.value)
        response = responder.send_response()
        return jsonify(content.to_dict())
        return render_template("quest_renderer.html", content=content.to_dict())            
    except ParsingError as e:
        return (jsonify({'error': str(e)}),
                StatusCode.UNAUTHORIZED.value)
    except AuthenticationError as e:
        return (jsonify({'error': str(e)}),
                StatusCode.UNAUTHORIZED.value)