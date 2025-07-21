import pytest
from flask import Flask, request

from app.errors import ValidationError
from app.enums import ParserKey, InputLocation
from app.request_management.validator.validator import Validator
from app.request_management.parser.parser import Parser
from app.game.quests.welcome import welcome_Q

app = Flask(__name__)

def test_welcome_q_setup():
    with app.test_request_context(
            path=('/game/welcome')
        ):
        settings = Parser.parse_quest_settings(welcome_Q)
        
        parsed = Parser.parse_request(request)
        
        assert Validator.validate_request(parsed, settings) == True