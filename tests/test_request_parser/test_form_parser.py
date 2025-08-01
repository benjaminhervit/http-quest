from app.parsers import RequestParser as Parser
from app.enums import ParserKey, QuestKey
import pytest
from flask import Flask, request

app = Flask(__name__)

def test_no_form_returns_empty_dict():
    with app.test_request_context(
        ):
        parsed = Parser.parse_form(request)
        assert isinstance(parsed, dict)
        assert parsed == {}
        
def test_valid_returns_expected():
    test_input = {'foo': 'bar'}
    with app.test_request_context(
        method='POST',
        data=test_input
        ):
        parsed = Parser.parse_form(request)
        assert isinstance(parsed, dict)
        assert parsed == test_input
        
def test_wrong_method_returns_empty():
    test_input = {'foo': 'bar'}
    with app.test_request_context(
        method='GET',
        data=test_input
        ):
        parsed = Parser.parse_form(request)
        assert isinstance(parsed, dict)
        assert not parsed
        assert parsed == {}