import pytest

from app.errors import ValidationError
from app.request_management import Validator

@pytest.mark.parametrize("keys, parsed_data, raises_exception, expected_result",
                         [
                             (['username'], {'username': 'test'}, False, True), #valid
                             (['username', 'foo'], {'username': 'test', 'foo': 'bar'}, False, True), #valid
                             (['username'], {}, True, None), #raise error on missing key in data
                             ([], {'foo': 'bar'}, True, None), #raise error on missing keys but found data
                             (['username'], {'username': 'test', 'foo': 'bar'}, True, None), #raise error keys and data not equal
                             (['username', 'fo'], {'username': 'test', 'foo': 'bar'}, True, None), #raise error keys and data not equal
                          ])
def test_keys_data_validator(keys, parsed_data,
                             raises_exception, expected_result):
    """unit testing of method that validates all parsed data.
    json, form, query validators are wrappers for better readability
    and potential changes in the future
    """
    
    # has keys and valid data
    if raises_exception:
        with pytest.raises(ValidationError):
            result = Validator.check_for_key_data_match(
                keys, parsed_data, "test")
    else:
        result = Validator.check_for_key_data_match(
            keys, parsed_data, "test")
        assert result == expected_result

def test_valid_method_check():
    # valid empty and GETs
    result = Validator.validate_method_data('GET', ['GET'])
    assert result is True
    
    result = Validator.validate_method_data('GET', ['GET', 'POST'])
    assert result is True
    
    with pytest.raises(ValidationError):
        result = Validator.validate_method_data('POST', ['GET'])