"""
Unit testing of the parsing strategies.
The testing relies on flasks test_request_context.
Strategies implement some extra rules just to be sure that
some standard rules, e.g. no Form together with GET.
"""

import pytest
from flask import Flask, request

import app.request_management.parser.request_strategies as ParseStrat

from app.enums import ReqMethodType
from app.errors import ParsingError

app = Flask(__name__)

def test_get_username_from_query():
    # valid
    with app.test_request_context(
            path=('/?username=test'),
        ):
        username = ParseStrat.get_username_from_query(request)
        assert username == 'test'
        
    # invalid
    with app.test_request_context(
            path=('/?user=test'),
        ):
        username = ParseStrat.get_username_from_query(request)
        assert username is None
        
    # no query
    with app.test_request_context(
            path=('/'),
        ):
        username = ParseStrat.get_username_from_query(request)
        assert username is None

def test_get_path():
    # empty path
    with app.test_request_context(
            path=('/'),
        ):
        path = ParseStrat.get_path(request)
        assert path == []
    
    # no path
    with app.test_request_context(
            path=(''),
        ):
        path = ParseStrat.get_path(request)
        assert path == []
        
    # single
    with app.test_request_context(
            path=('/index'),
        ):
        path = ParseStrat.get_path(request)
        assert path == ['index']
        
    # four 
    with app.test_request_context(
            path=('/index/a/b/c/'),
        ):
        path = ParseStrat.get_path(request)
        assert path == ['index', 'a', 'b', 'c']
        assert sorted(path) == sorted(['index', 'a', 'b', 'c'])
        
    # no queries caught in path pt. 1 - w. /
    with app.test_request_context(
            path=('index/?username=test'),
        ):
        path = ParseStrat.get_path(request)
        assert path == ['index']
        
        
    # no queries caught in path pt. 2 - w.o. /
    with app.test_request_context(
            path=('index?username=test'),
        ):
        path = ParseStrat.get_path(request)
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
    #flask auto-formats to form with POST
    with app.test_request_context(
            path=('/'),
            method='POST',
            data={'foo': 'bar',
                  'key': '123'}
        ):
        form = ParseStrat.get_form(request)
        assert form == {'foo': 'bar', 'key': '123'}
        
    #valid method with empty data should return None
    with app.test_request_context(
            path=('/'),
            method='POST',
            data={}
        ):
        form = ParseStrat.get_form(request)
        assert form is None
        
    #no data should return None
    with app.test_request_context(
            path=('/'),
            method='POST'
        ):
        form = ParseStrat.get_form(request)
        assert form is None
        
    #parser should not allow forms send with GET
    with app.test_request_context(
            path=('/'),
            method='GET',
            data={'foo': 'bar'}
        ):
        form = ParseStrat.get_form(request)
        assert form is None

def test_get_query():
    #valid single value
    with app.test_request_context(
            path=('/?username=test'),
            method='get',
        ):
        query = ParseStrat.get_query(request)
        assert isinstance(query, dict)
        assert query.get('username') == 'test'
        assert sorted(query.keys()) == ['username']
    
    #valid double value
    with app.test_request_context(
            path=('/?username=test&key=123'),
            method='get',
        ):
        query = ParseStrat.get_query(request)
        assert isinstance(query, dict)
        assert query.get('username') == 'test'
        assert query.get('key') == '123'
        assert sorted(query.keys()) == sorted(['username', 'key'])
    
    #no query returns none
    with app.test_request_context(
            path=('/'),
            method='get',
        ):
        query = ParseStrat.get_query(request)
        assert query is None
    
    #invalid double value: using ? instead of &
    with app.test_request_context(
            path=('/?username=test?key=123'),
            method='get',
        ):
        query = ParseStrat.get_query(request)
        assert isinstance(query, dict)
        assert query.get('username') != 'test'
        assert query.get('username') == 'test?key=123'
        assert sorted(query.keys()) == sorted(['username'])
        
    #invalid double value: using &? instead of &
    with app.test_request_context(
            path=('/?username=test&?key=123'),
            method='get',
        ):
        query = ParseStrat.get_query(request)
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
        query = ParseStrat.get_query(request)
        assert isinstance(query, dict)
        assert query.get('username') == 'test'
        assert query.get('key') is None
        assert query.get('?key') == '123'
        assert sorted(query.keys()) != sorted(['username', 'key'])
        assert sorted(query.keys()) == sorted(['username', '?key'])

def test_get_json():
    #json with values
    with app.test_request_context(
            path=('/'),
            method='get',
            json={'key': 'value'}
        ):
            parsed_json = ParseStrat.get_json(request)
            assert parsed_json == {'key': 'value'}
            assert isinstance(parsed_json, dict)
    
    #empty json should return None
    json_data = {}
    with app.test_request_context(
            path=('/'),
            method='get',
            json={}
        ):
            parsed_json = ParseStrat.get_json(request)
            assert parsed_json is None
            
    #no json setup should return None
    with app.test_request_context(
            path=('/'),
            method='get',
        ):
            parsed_json = ParseStrat.get_json(request)
            assert parsed_json is None

@pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'get', 'post', 'put', 'delete'])
def test_get_method(method: str):
    # ACCEPTED ENUMS
    with app.test_request_context(
        path=('/'),
        method=method
    ):
        parsed = ParseStrat.get_method(request)
        assert parsed == method.upper()  #flask capitalize automatically
        assert parsed in ReqMethodType
        assert isinstance(parsed, str)
        
    # INVALID
    # no method will return GET
    with app.test_request_context(
        path=('/')
    ):
        method = ParseStrat.get_method(request)
        assert method == 'GET'
        assert method in ReqMethodType
    
    # gibberish
    with app.test_request_context(
        path=('/'),
        method='NONSENSE'
    ):
        with pytest.raises(ParsingError) as exc_info:
            method = ParseStrat.get_method(request)
        assert 'Request method (NONSENSE) is not accepted' in str(exc_info.value)