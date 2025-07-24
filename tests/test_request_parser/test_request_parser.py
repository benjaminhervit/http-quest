import pytest
from flask import Flask, request

from app.parsers import RequestParser as Parser
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

def test_key_values():
    # valid
    with app.test_request_context(
        ):
        parsed = Parser.parse(request)
        keys = parsed.keys()
        assert ParserKey.METHOD_DATA.value in keys
        assert ParserKey.QUERY_DATA.value in keys
        assert ParserKey.PATH_DATA.value in keys
        # assert ParserKey.FORM_DATA.value in keys
        # assert ParserKey.JSON_DATA.value in keys
        # assert ParserKey.HEADERS_DATA.value in keys
        # assert ParserKey.USERNAME.value in keys