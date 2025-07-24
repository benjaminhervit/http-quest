import pytest
from flask import Flask, request

from app.parsers import RequestParser as Parser
from app.enums import ParserKey, QuestKey

app = Flask(__name__)

def req_with_query_returns_dict_in_query_key():
    with app.test_request_context(
        path="?foo=bar"
        ):
        parsed = Parser.parse(request)
        query_data = parsed.get(ParserKey.QUERY_DATA)
        assert isinstance(query_data, dict)
        assert query_data == {'foo': 'bar'}

def empty_query_returns_empty_dict():
    with app.test_request_context(
        ):
        parsed = Parser.parse(request)
        assert parsed.get(ParserKey.QUERY_DATA) == {}

def test_all_parsed_keys_are_valid_enums():
    
    with app.test_request_context(
        ):
        parsed = Parser.parse(request)
        
        for k,v in parsed.items():
            assert k in ParserKey

def test_key_values():
    
    with app.test_request_context(
        ):
        parsed = Parser.parse(request)
        keys = parsed.keys()
        required_keys = [ParserKey.METHOD_DATA, ParserKey.QUERY_DATA,
                         ParserKey.PATH_DATA]
        
        assert set(required_keys).issubset(keys)