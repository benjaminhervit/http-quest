from typing import Optional
from flask import request, jsonify

from app.blueprints.quest import bp
from app.errors import ParsingError, ValidationError, AuthenticationError, GameError, QuestError
from app.enums import StatusCode, ParserKey

from app.models.quest import Quest
from app.models.user_quest_state import UserQuestState as UQState

from app.request_management.parser.factory import create_parser
from app.request_management.parser.parser import Parser
from app.request_management.validator.factory import create_validator
from app.request_management.validator.validator import Validator
from app.request_management.authenticator.factory import create_authenticator
from app.request_management.authenticator.authenticator import Authenticator

from app.game.game_manager import GameManager


@bp.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
def welcome(path):
    return "This is just a game. if you welcome with a name you can come further."


@bp.route('<quest_slug>', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('<quest_slug>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def quest(quest_slug, path):
    try:
        quest_data = Quest.get_by_slug(quest_slug)
        if not isinstance(quest_data, Quest):
            raise QuestError('Could not find quest. Check if you got the path right or talk with the developer.', code=StatusCode.SERVER_ERROR)
        
        # PARSE
        parser: Parser = create_parser(
            quest_data.input_loc,
            quest_data.username_loc,
            quest_data.token_loc)
        
        parsed: dict = parser.parse_request(
            req=request, path=path,
            answer_key=quest_data.answer_key)
        
        validator = Validator(['GET', 'POST'], [], 'NONE', 'NONE', 'NONE')
        
        print(f"parsed:\n {parsed}")
        return "testing"
        
        # #VALIDATE
        # validator: Validator = create_validator(
        #     quest_data.answer_loc,
        #     quest_data.username_loc,
        #     quest_data.token_loc)
        
        # parsed = validator.validate(parsed=parsed)
        
        # #AUTHENTICATE
        # authenticator: Authenticator = create_authenticator(
        #     quest_data.auth_type
        #     )
        # authenticator.authenticate(parsed=parsed)
        
        # #RUN QUEST
        # user_inputs: str = parsed.get(ParserKey.ANSWER.value, "")
        # username: str = parsed.get(ParserKey.USERNAME.value, "")
        # quest_state = UQState.get_uqs(
        #     username=username, 
        #     slug=quest_data.slug
        #     )
        
        # if quest_state is None:
        #     raise GameError(f'Could not retreive quest state with usernae: '
        #                     f'{username}, slug:{quest_data.slug}')
        
        # GM = GameManager(quest_data=quest_data,
        #                  user_answer=user_inputs,
        #                  username=username,
        #                  state=quest_state.state)
        # GM.run_quest()
        
        # #UPDATE USER:QUEST SESSION DATA
        # state: str = GM.get_end_state()
        # UQState.update_state(state, quest_state)
        # UQState.unlock_next_quests(quest_data, quest_state, username)

        # response = GM.get_response()
        # if response is None:
        #     raise GameError('Game manager did not create any response', 
        #                     code=StatusCode.SERVER_ERROR)
        
        # return jsonify(response, StatusCode.OK)
        
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