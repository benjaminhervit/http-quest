from enum import Enum

from app.utils import get_enum_values_as_list

def test_empty_enum_returns_empty_list():
    class testEnum(str, Enum):
        pass
    
    assert get_enum_values_as_list(testEnum) == []
    
def test_retuns_all_values():
    class testEnum(str, Enum):
        A = "A"
        B = "B"
    
    assert get_enum_values_as_list(testEnum) == ['A', 'B']
