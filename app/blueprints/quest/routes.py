from typing import Optional
from flask import request, jsonify

from app.blueprints.quest import bp
from app.errors import (ParsingError, ValidationError, 
                        AuthenticationError, GameError, QuestError)

from app.enums import StatusCode, ParserKey

from app.models import Quest, UserQuestState, User

from app.game.game_manager.factory import create_game_manager
from app.request_manager import RequestManager
# from app.request_manager import (RequestParser, QuestParser,
#                                  Validator, create_authenticator)

@bp.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
def welcome(path):
    return "This is just a game. if you welcome with a name you can come further."


@bp.route('<quest_slug>', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('<quest_slug>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def quest(quest_slug, path):
    try:
        quest = Quest.get_by_slug(quest_slug)
        if not isinstance(quest, Quest):
            raise QuestError('Could not find quest. Check if you got the path right or talk with the developer.', code=StatusCode.SERVER_ERROR)
        
        parsed = RequestManager.handle(request, quest)
        
        gm = create_game_manager(quest, parsed)
        gm.run_quest()
        
        if not quest.is_stateless:
            uqs = UserQuestState.get_uqs(gm.user_name, quest.slug) 
            if not isinstance(uqs, UserQuestState):
                raise ImportError('Could not ')
            UserQuestState.update_state(gm.get_end_state(), uqs=uqs)
        return gm.get_response(), StatusCode.OK.value
    
    except ImportError as e:
        return jsonify({str(e)}), StatusCode.SERVER_ERROR
    except QuestError as e:
        return jsonify({'error': f'Quest error: {str(e)}'}, e.code)
    except ParsingError as e:
        return jsonify({'error': f'Parsing error: {str(e)}'}, e.code)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}, e.code)
    except AuthenticationError as e:
        return jsonify({'error': f'Authentication error: {str(e)}'}, e.code)
    except GameError as e:
        return jsonify({'error': f'Game error error: {str(e)}'}, e.code)