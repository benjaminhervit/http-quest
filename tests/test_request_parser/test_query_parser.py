from app.parsers import RequestParser as Parser
from app.enums import ParserKey, QuestKey
import pytest
from flask import Flask, request

app = Flask(__name__)

def test_no_query_returns_empty_dict():
    with app.test_request_context(
        ):
        parsed = Parser.parse(request)
        query_data = parsed.get(ParserKey.QUERY_DATA)
        assert isinstance(query_data, dict)
        assert query_data == {}
        
def test_data_stored_in_query_key():
    with app.test_request_context(
        path="?foo=bar"
        ):
        parsed = Parser.parse(request)
        query_data = parsed.get(ParserKey.QUERY_DATA)
        assert query_data == {'foo': 'bar'}