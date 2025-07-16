import pytest

import app.request_management.parser as Parser
from app.enums import ParsingKey, InputLocation
from app.errors import ParsingError, ValidationError

def test_get_correct_answer():
    from app.errors import ParsingError
    
    t = {
        'CORRECT_ANSWER':'A'
    }
    r = Parser._get_correct_answer(t)
    assert r == 'A'
    
    t = {
        ParsingKey.CORRECT_ANSWER.value:'B'
    }
    r = Parser._get_correct_answer(t)
    assert r == 'B'
    
    t = {
        'ABC' : 'B'
    }
    with pytest.raises(ParsingError) as exc_info:
        Parser._get_correct_answer(t)
    assert 'Could not find correct answer to quest' in str(exc_info.value)
    
def test_get_location():
    
    #PASS: key exists and value is valid
    key = 'k'
    loc = 'FORM'
    t = {
        key:loc
    }
    r = Parser._get_location(key, t)
    assert r == loc
    
    #PASS: key exists and value is valid and derived from enum
    key = 'k'
    loc = InputLocation.FORM.value
    t = {
        key:loc
    }
    r = Parser._get_location(key, t)
    assert r == loc
    
    #FAIL: key does not exist, value is valid from enum
    key = 'k'
    loc = InputLocation.FORM.value
    t = {
        'ABC' : loc
    }
    with pytest.raises(ValidationError) as exc_info:
        Parser._get_location(key, t)
    assert 'Could not find valid lcoation' in str(exc_info.value)
    
    #FAILD: key esist but value is enum instead of enum.value
    key = 'k'
    loc = InputLocation.FORM
    t = {
        key: InputLocation.FORM
    }
    with pytest.raises(ValidationError) as exc_info:
        Parser._get_location(key, t)
    assert 'Could not find valid lcoation' in str(exc_info.value)
    