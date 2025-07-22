import pytest
from flask import Flask, request

from app.request_management import Parser
from app.enums import ParserKey

app = Flask(__name__)

@pytest.fixture
def base_quest_settings() -> dict:
    return {
            ParserKey.METHOD_DATA: ['GET'],
            ParserKey.JSON_KEYS: None,
            ParserKey.QUERY_KEYS: None,
            ParserKey.FORM_KEYS: None,
            ParserKey.HEADERS_KEYS: None,
            ParserKey.USERNAME_LOC: None,
            ParserKey.TOKEN_LOC: None,
            ParserKey.INPUT_LOC: None,
            ParserKey.AUTH_TYPE: None,
            ParserKey.ANSWER_KEY: None
        }

def test_cleaned_parse_with_query(base_quest_settings):
            
    #only get and query
    base_quest_settings[ParserKey.QUERY_KEYS] = 'username'
    with app.test_request_context(
        path='/?username=test'
        ):
        parsed = Parser.parse_request(request)
        filtered = Parser.get_filtered_parse(parsed, base_quest_settings)
        assert len(filtered) == 2
        assert set(filtered.keys()) == {ParserKey.METHOD_DATA, 
                                        ParserKey.QUERY_DATA}
        
        query_content = filtered.get(ParserKey.QUERY_DATA)
        assert query_content is not None
        key = base_quest_settings[ParserKey.QUERY_KEYS]
        assert query_content[key] == 'test'
        assert len(query_content) == 1
        

def test_filtered_parse(base_quest_settings):
    #only get
    with app.test_request_context(
        path='/'
        ):
        parsed = Parser.parse_request(request)
        filtered = Parser.get_filtered_parse(parsed, base_quest_settings)
        assert filtered is not None
        assert set(filtered.keys()) == {ParserKey.METHOD_DATA}
        assert filtered.get(ParserKey.METHOD_DATA) == 'GET'

def test_key_values():
    # valid
    with app.test_request_context(
        ):
        parsed = Parser.parse_request(request)
        keys = parsed.keys()
        assert ParserKey.METHOD_DATA.value in keys
        assert ParserKey.QUERY_DATA.value in keys
        assert ParserKey.PATH_DATA.value in keys
        # assert ParserKey.FORM_DATA.value in keys
        # assert ParserKey.JSON_DATA.value in keys
        # assert ParserKey.HEADERS_DATA.value in keys
        # assert ParserKey.USERNAME.value in keys