from flask import Request
import logging

from app.enums import StatusCode, ParserKey
from app.errors import ValidationError, AuthenticationError
from app.models import Quest

from app.validator import Validator
from app.parsers import QuestParser, RequestParser
from app.request_manager.request_context import RequestContext
from app.game.state_manager.factory import create_state_manager
from app.game.state_manager.state_manager import StateManager
from app.game.game_manager.quest_manager import QuestManager
from app.authenticator.factory import create_authenticator

log = logging.getLogger(__name__)
# TODO: setup log events

class RequestManager:
    @staticmethod
    def handle(request: Request, quest: Quest) -> RequestContext:
        
        # PARSE
        parsed = RequestParser.parse(request)
        
        # VALIDATE
        settings: dict = QuestParser.get_settings(quest)
        if not Validator.validate_request(parsed, settings):
            raise ValidationError(f'Could not successfully validate'
                                  f'{quest.title} with parsed data: \n'
                                  f'{parsed} settings: {settings}',
                                  code=StatusCode.BAD_REQUEST)
        
        # AUTHENTICATE    
        auth = create_authenticator(quest.auth_type)
        identify = auth.get_identity(parsed, settings)
        auth_result = auth.authenticate(identify)
        success, user = auth_result.success, auth_result.user
        if not success:
            raise AuthenticationError('Could not authenticate player with '
                                      f'auth_type: {quest.auth_type}'
                                      f'and parsed data: {parsed}',
                                      code=StatusCode.BAD_REQUEST)
        
        state_manager: StateManager = create_state_manager(quest.is_stateless)
        state = state_manager.get_start_state(quest, user)
        user_input = {}
        method = parsed.get(ParserKey.METHOD_DATA)
        
        # BUILD CONTEXT
        context = RequestContext(
            user=user,
            parsed=parsed,
            quest=quest,
            state=state.value
        )
        
        # EXECUTE QUEST
        gm = QuestManager(context)
        gm.run()
        response = gm.get_response()
        
        # UPDATE QUEST STATE
        # TODO: split up quest state and session outcome so that response and end state are independent
        end_state = state_manager.get_end_state(gm.state)
        username = user.username if user else ""
        state_manager.update_quest_state(new_state=end_state.value,
                                         username=username,
                                         slug=quest.slug)
        
        return response