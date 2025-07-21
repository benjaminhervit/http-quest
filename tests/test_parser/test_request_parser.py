import pytest
from flask import Flask, request

import app.request_management.parser.request_strategies as ParseStrat
from app.request_management.parser.parser import Parser

from app.enums import ReqMethodType, ParserKey
from app.errors import ParsingError

app = Flask(__name__)

@pytest.fixture
def base_parser() -> Parser:
    return Parser(method_fn=ParseStrat.get_method,
                  path_fn=ParseStrat.get_path,
                  query_fn=ParseStrat.get_query,
                  json_fn=ParseStrat.get_json,
                  form_fn=ParseStrat.get_form,
                  header_fn=ParseStrat.get_headers,
                  username_fn=ParseStrat.get_none,
                  token_fn=ParseStrat.get_none,
                  input_fns=ParseStrat.get_none)

def test_key_values(base_parser):
    # valid
    with app.test_request_context(
        ):
        parsed = base_parser.parse_request(request)
        keys = parsed.keys()
        assert ParserKey.METHOD_DATA.value in keys
        assert ParserKey.FORM_DATA.value in keys
        assert ParserKey.JSON_DATA.value in keys
        assert ParserKey.PATH_DATA.value in keys
        assert ParserKey.QUERY_DATA.value in keys
        assert ParserKey.HEADERS_DATA.value in keys
        assert ParserKey.USERNAME.value in keys

def test_username_with_value(base_parser):
    # VALID QUERY
    base_parser.username_fn = ParseStrat.get_username_from_query
    with app.test_request_context(
        path='/?username=test'
        ):
        parsed = base_parser.parse_request(request)
        assert parsed.get(ParserKey.USERNAME) == 'test'
    # INVALID QUERY
    base_parser.username_fn = ParseStrat.get_username_from_query
    with app.test_request_context(
        path='/?user=test'
        ):
        parsed = base_parser.parse_request(request)
        assert parsed.get(ParserKey.USERNAME) is None
        
    # VALID FORM WITH POST
    base_parser.username_fn = ParseStrat.get_username_from_form
    with app.test_request_context(
        path='/',
        method='POST',
        data={'username': 'test'}
        ):
        parsed = base_parser.parse_request(request)
        assert parsed.get(ParserKey.USERNAME.value) == 'test'
        
    # VALID FORM WITH POST
    base_parser.username_fn = ParseStrat.get_username_from_json
    with app.test_request_context(
        path='/',
        method='POST',
        json={'username':'test'}
        ):
        parsed = base_parser.parse_request(request)
        assert parsed.get(ParserKey.USERNAME.value) == 'test'
        
    # USERNAME IN THE WRONG LOCATIN
    base_parser.username_fn = ParseStrat.get_username_from_json
    with app.test_request_context(
        path='/',
        method='POST',
        data={'username': 'test'}  # data instead of json
        ):
        parsed = base_parser.parse_request(request)
        assert parsed.get(ParserKey.USERNAME.value) is None