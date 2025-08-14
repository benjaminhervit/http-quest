from flask import request, jsonify

from app.blueprints.quests import bp
from app.errors import (
    ParsingError,
    ValidationError,
    AuthenticationError,
    GameError,
    QuestError,
)

from app.enums import StatusCode
from app.models import Quest

# from app.request_manager import RequestManager


@bp.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
def welcome(path):
    return "This is just a game. Extend welcome on your path and you can begin."


# @bp.route('<quest_slug>', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
# @bp.route('<quest_slug>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def quest(quest_slug, path):
#     try:
#         quest_m = Quest.get_by_slug(quest_slug)
#         if not isinstance(quest_m, Quest):
#             raise QuestError('Could not find quest. Check path '
#                              'or talk with the developer.',
#                              code=StatusCode.SERVER_ERROR)

#         return jsonify(RequestManager.handle(request, quest_m), StatusCode.OK)

#     except ImportError as e:
#         return jsonify({'error': str(e)}), StatusCode.SERVER_ERROR
#     except QuestError as e:
#         return jsonify({'error': f'Quest error: {str(e)}'}, e.code)
#     except ParsingError as e:
#         return jsonify({'error': f'Parsing error: {str(e)}'}, e.code)
#     except ValidationError as e:
#         return jsonify({'error': f'Validation error: {str(e)}'}, e.code)
#     except AuthenticationError as e:
#         return jsonify({'error': f'Authentication error: {str(e)}'}, e.code)
#     except GameError as e:
#         return jsonify({'error': f'Game error error: {str(e)}'}, e.code)
