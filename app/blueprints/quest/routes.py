from flask import request, jsonify

from app.blueprints.quest import bp

from app.errors import ParsingError, ValidationError, AuthenticationError, GameError, QuestError
from app.enums import StatusCode, ParserKey

# from app.game.quests import quests
# from app.game.quests.quest_data import QuestData
from app.models.quest import Quest
# from app.game.quests.mode_quests.welcome import welcome_Q

from app.request_management.parser.factory import create_parser
from app.request_management.parser.parser import Parser

from app.request_management.validator.factory import create_validator
from app.request_management.validator.validator import Validator

from app.request_management.authenticator.factory import create_authenticator
from app.request_management.authenticator.authenticator import Authenticator

from app.game.game_manager.game_manager import GameManager


@bp.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
def welcome(path):
    return "This is just a game. if you welcome with a name you can come further."


@bp.route('<quest_title>', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('<quest_title>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def quest(quest_title, path):
    try:
        # quest_id = f"{quest_title}_{request.method}"
        # quest_obj: QuestData | None = quests.get(quest_id)
        quest_obj: Quest = Quest.query.filter_by(slug=quest_title).first()
        
        if not quest_obj:
            raise QuestError('Could not find quest. Check if you got the path right or talk with the developer.', code=StatusCode.SERVER_ERROR)
        
        print(quest_obj.as_dict())
        
        #PARSE
        parser: Parser = create_parser(
            quest_obj.answer_loc, 
            quest_obj.username_loc,
            quest_obj.token_loc)
        parsed: dict = parser.parse(
            req=request, path=path,
            answer_key=quest_obj.answer_key)
        
        #VALIDATE
        validator: Validator = create_validator(
            quest_obj.answer_loc,
            quest_obj.username_loc,
            quest_obj.token_loc)
        
        validator.validate(parsed=parsed)
        
        #AUTHENTICATE
        authenticator: Authenticator = create_authenticator(
            quest_obj.auth_type
            )
        authenticator.authenticate(parsed=parsed)
        
        #RUN QUEST
        user_inputs = parsed.get(ParserKey.ANSWER.value)
        username = parsed.get(ParserKey.USERNAME.value)
        
        GM = GameManager(quest_data=quest_obj, 
                         user_answer=user_inputs, 
                         username=username)
        GM.run_quest()
        
        #UPDATE USER:QUEST SESSION DATA
        state = GM.get_state()
        #TODO: implement db model/table for user:quest state
        
        response = GM.get_response()
        if response is None:
            raise GameError('Game manager did not create any response', 
                            code=StatusCode.SERVER_ERROR)
        
        return jsonify(response, StatusCode.OK)
        return "woho"
        
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