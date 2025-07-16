from flask import request, jsonify

from app.blueprints.quest import bp

from app.request_management.parsed_request import ParsedRequest
import app.request_management.parser as Parser
import app.request_management.authentication as Authenticator
from app.errors import ParsingError, ValidationError, AuthenticationError, GameError, QuestError
from app.enums import StatusCode

from app.game.quests import quests
from app.game.quests.quest_data import QuestData
import app.game.game_manager as GameManager

@bp.route('/', defaults={'path':''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
def welcome(path):
    return "This is just a game. if you welcome with a name you can come further."

@bp.route('<quest_id>', defaults={'path':''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('<quest_id>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def quest(quest_id, path):
    try:
        quest_obj: QuestData= quests.get(quest_id)
        if not quest_obj:
            raise QuestError('Could not find quest. Check if you got the path right or talk with the developer.', code=StatusCode.SERVER_ERROR)
        
        parsed:ParsedRequest = Parser.parse(request, quest_obj.request_settings, path)
        Authenticator.auth(parsed)
        response = GameManager.execute_quest(quest_obj, parsed)
        return jsonify(response, StatusCode.OK)
        
    except QuestError as e:
        return jsonify({'error':f'Quest error: {str(e)}'},e.code)
    except ParsingError as e:
        return jsonify({'error':f'Parsing error: {str(e)}'},e.code)
    except ValidationError as e:
        return jsonify({'error':f'Validation error: {str(e)}'},e.code)
    except AuthenticationError as e:
        return jsonify({'error':f'Authentication error: {str(e)}'},e.code)
    except GameError as e:
        return jsonify({'error':f'Game error error: {str(e)}'},e.code)