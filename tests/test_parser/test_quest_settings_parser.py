"""
Unit testing of the parsing strategies.
The testing relies on flasks test_request_context.
Strategies implement some extra rules just to be sure that
some standard rules, e.g. no Form together with GET.
"""

import pytest
from flask import Flask, request

from app.enums import ParserKey, InputLocation
from app.errors import ParsingError
from app.models.quest import Quest
from app.request_management.parser.parser import Parser

app = Flask(__name__)

@pytest.fixture
def minimum_test_quest() -> Quest:
    return Quest(
        title="...",
        story=("..."),
        directions="...",
        quest="...",

        success_response="...",
        failed_response="...",
        is_locked_response="...",
        is_completed_response="...",
        
        allowed_req_methods="GET"
    )

def test_keys_with_values(minimum_test_quest):
    minimum_test_quest.form_keys = "form"
    minimum_test_quest.query_keys = "query"
    minimum_test_quest.json_keys = "json"
    minimum_test_quest.headers_keys = "headers"
    
    minimum_test_quest.answer_key = "answer_key_value"
    minimum_test_quest.input_loc = "input_loc_value"
    
    minimum_test_quest.auth_type = "auth_type_value"
    minimum_test_quest.username_loc = "FORM_DATA"
    minimum_test_quest.token_loc = "HEADERS_DATA"
    
    minimum_test_quest.allowed_req_methods = "GET,POST,PUT,DELETE"
    
    #  check methods
    parsed: dict = Parser.parse_quest_settings(minimum_test_quest)
    assert isinstance(parsed, dict)
    methods: list[str] | None = parsed.get(ParserKey.ALLOWED_REQ_METHODS)
    assert isinstance(methods, list)
    assert sorted(methods) == sorted(['GET', 'POST', 'PUT', 'DELETE'])
    
    #check keys
    assert parsed.get(ParserKey.FORM_KEYS) == 'form'
    assert parsed.get(ParserKey.QUERY_KEYS) == 'query'
    assert parsed.get(ParserKey.JSON_KEYS) == 'json'
    assert parsed.get(ParserKey.HEADERS_KEYS) == 'headers'
    
    #auth
    assert parsed.get(ParserKey.AUTH_TYPE) == 'auth_type_value'
    
    #input
    assert parsed.get(ParserKey.INPUT_LOC) == 'input_loc_value'
    
    #answer_key
    assert parsed.get(ParserKey.ANSWER_KEY) == 'answer_key_value'
    
    #username 
    username_key_value = parsed.get(ParserKey.USERNAME_LOC)
    assert username_key_value == 'FORM_DATA'
    assert ParserKey(username_key_value) in ParserKey
    
    #tokeb 
    token_key_value = parsed.get(ParserKey.TOKEN_LOC)
    assert token_key_value == 'HEADERS_DATA'
    assert ParserKey(token_key_value) in ParserKey
    

def test_get_quest_methods(minimum_test_quest):
    """Most errors are caight by sql alchemy. See Model validation
    """
    # multi methods
    minimum_test_quest.allowed_req_methods = 'GET,POST'
    parsed = Parser.parse_quest_settings(minimum_test_quest)
    assert parsed.get(ParserKey.ALLOWED_REQ_METHODS) == ['GET', 'POST']
    
def test_parse_quest_settings_with_minimum_quest_settings(minimum_test_quest):
    parsed = Parser.parse_quest_settings(minimum_test_quest)
    assert parsed.get(ParserKey.ALLOWED_REQ_METHODS) == ['GET']
    assert parsed.get(ParserKey.ALLOWED_REQ_METHODS) != ['get']
    assert parsed.get(ParserKey.QUERY_KEYS) is None
    assert parsed.get(ParserKey.JSON_KEYS) is None
    assert parsed.get(ParserKey.FORM_KEYS) is None
    assert parsed.get(ParserKey.HEADERS_KEYS) is None
    assert parsed.get(ParserKey.USERNAME_LOC) is None
    assert parsed.get(ParserKey.ANSWER_KEY) is None
    assert parsed.get(ParserKey.INPUT_LOC) is None
    assert parsed.get(ParserKey.TOKEN_LOC) is None