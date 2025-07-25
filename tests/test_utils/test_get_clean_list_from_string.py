import pytest

from app.utils import get_clean_list_from_string

def test_empty_string_returns_empty_list():
    s = ''
    assert get_clean_list_from_string(s, ',') == []
    
def test_empty_values_are_removed():
    s = 'a,,c'
    assert get_clean_list_from_string(s, ',') == ['a', 'c']
    
def test_valid_values_are_included():
    s = 'a,b,c'
    assert get_clean_list_from_string(s, ',') == ['a', 'b', 'c']