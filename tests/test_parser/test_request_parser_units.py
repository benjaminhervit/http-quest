"""
Unit testing of the parsing strategies.
The testing relies on flasks test_request_context.
Strategies implement some extra rules just to be sure that
some standard rules, e.g. no Form together with GET.
"""

import pytest
from flask import Flask, request
from app.request_management import Parser
from app.enums import ReqMethodType
from app.errors import ParsingError

app = Flask(__name__)

def test_get_path():
    # empty path
    with app.test_request_context(
            path=('/'),
        ):
        path = Parser.parse_path(request)
        assert path == []
    
    # no path
    with app.test_request_context(
            path=(''),
        ):
        path = Parser.parse_path(request)
        assert path == []
        
    # single
    with app.test_request_context(
            path=('/index'),
        ):
        path = Parser.parse_path(request)
        assert path == ['index']
        
    # four 
    with app.test_request_context(
            path=('/index/a/b/c/'),
        ):
        path = Parser.parse_path(request)
        assert path == ['index', 'a', 'b', 'c']
        assert sorted(path) == sorted(['index', 'a', 'b', 'c'])
        
    # no queries caught in path pt. 1 - w. /
    with app.test_request_context(
            path=('index/?username=test'),
        ):
        path = Parser.parse_path(request)
        assert path == ['index']
        
        
    # no queries caught in path pt. 2 - w.o. /
    with app.test_request_context(
            path=('index?username=test'),
        ):
        path = Parser.parse_path(request)
        assert path == ['index']
        
def test_get_headers():
    #TODO: will begin unit testing together with relevant quests.
    return None

def test_ReqMethodType():
    #validate that it is possible to check strings directly against enums and not only their values
    assert 'GET' == ReqMethodType.GET
    assert 'GET' == ReqMethodType.GET.value
    assert ReqMethodType.GET == 'GET'
    assert ReqMethodType('GET') == ReqMethodType.GET

def test_get_form():
    # TODO: will begin unit testing with relevant quests
    return None

def test_get_query():
    #valid single value
    with app.test_request_context(
            path=('/?username=test'),
            method='get',
        ):
        query = Parser.parse_query(request)
        assert isinstance(query, dict)
        assert query.get('username') == 'test'
        assert sorted(query.keys()) == ['username']
    
    #valid double value
    with app.test_request_context(
            path=('/?username=test&key=123'),
            method='get',
        ):
        query = Parser.parse_query(request)
        assert isinstance(query, dict)
        assert query.get('username') == 'test'
        assert query.get('key') == '123'
        assert sorted(query.keys()) == sorted(['username', 'key'])
    
    #no query returns none
    with app.test_request_context(
            path=('/'),
            method='get',
        ):
        query = Parser.parse_query(request)
        assert not query
    
    #invalid double value: using ? instead of &
    with app.test_request_context(
            path=('/?username=test?key=123'),
            method='get',
        ):
        query = Parser.parse_query(request)
        assert isinstance(query, dict)
        assert query.get('username') != 'test'
        assert query.get('username') == 'test?key=123'
        assert sorted(query.keys()) == sorted(['username'])
        
    #invalid double value: using &? instead of &
    with app.test_request_context(
            path=('/?username=test&?key=123'),
            method='get',
        ):
        query = Parser.parse_query(request)
        assert isinstance(query, dict)
        assert query.get('username') == 'test'
        assert query.get('key') is None
        assert query.get('?key') == '123'
        assert sorted(query.keys()) != sorted(['username', 'key'])
        assert sorted(query.keys()) == sorted(['username', '?key'])
        
    #Does not pick up path in query
    with app.test_request_context(
            path=('/index/test/?username=test&?key=123'),
            method='get',
        ):
        query = Parser.parse_query(request)
        assert isinstance(query, dict)
        assert query.get('username') == 'test'
        assert query.get('key') is None
        assert query.get('?key') == '123'
        assert sorted(query.keys()) != sorted(['username', 'key'])
        assert sorted(query.keys()) == sorted(['username', '?key'])

def test_get_json():
    # TODO: Will begin together with relevant quests
    return None

@pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'get', 'post', 'put', 'delete'])
def test_get_method(method: str):
    # ACCEPTED ENUMS
    with app.test_request_context(
        path=('/'),
        method=method
    ):
        parsed = Parser.parse_method(request)
        assert parsed == method.upper()  #flask capitalize automatically
        assert parsed in ReqMethodType
        assert isinstance(parsed, str)
        
    # INVALID
    # no method will return GET
    with app.test_request_context(
        path=('/')
    ):
        parsed = Parser.parse_method(request)
        assert parsed == 'GET'
        assert parsed in ReqMethodType
    
    # gibberish will still be accepted by the parser
    with app.test_request_context(
        path=('/'),
        method='NONSENSE'
    ):
        parsed = Parser.parse_method(request)
        assert parsed == 'NONSENSE'