from flask import Request
import logging

from app.errors import ValidationError, AuthenticationError
from app.models import Quest, User
from app.authenticator.factory import create_authenticator
from app.validator import Validator
from app.parsers import QuestParser, RequestParser

log = logging.getLogger(__name__)
# TODO: setup log events

class RequestManager:
    @staticmethod
    def handle(request: Request, quest: Quest):
        
        # PARSE
        parsed = RequestParser.parse(request)
        
        # VALIDATE
        settings: dict = QuestParser.get_settings(quest)
        if not Validator.validate_request(parsed, settings):
            raise ValidationError(f'Could not successfully validate'
                                  f'{quest.title} with parsed data: \n'
                                  f'{parsed} settings: {settings}')
        
        # AUTHENTICATE    
        auth = create_authenticator(quest.auth_type)
        if not auth.authenticate(parsed):
            raise AuthenticationError('Could not authenticate player with '
                                      f'auth_type: {quest.auth_type}'
                                      f'and parsed data: {parsed}')
            
        return parsed