import pytest

from app.errors import ValidationError
from app.validator.validator import Validator
from app.enums import QuestKey, ParserKey


@pytest.mark.parametrize("settings, parsed, expects_error, error_msg",
                         [({'foo': 'bar'}, {ParserKey.METHOD_DATA: 'GET'}, True, "Found one or more setting keys that are not valid."),
                          ({QuestKey.METHOD_DATA: ['GET']}, {'foo': 'bar'}, True, "Found one or more setting keys that are not valid."),
                          ({QuestKey.METHOD_DATA: ['GET']}, {ParserKey.METHOD_DATA: 'GET'}, False, "")
                          ])
def test_validate_request_inputs(settings, parsed, expects_error, error_msg):
    #when keys in settings are not in QestKeys enum, then raise error
    if expects_error:
        with pytest.raises(ValueError) as exc:
            Validator.validate_request(parsed, settings)
        assert error_msg in str(exc) 
    else:
        assert Validator.validate_request(parsed, settings) is True

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
    if raises_exception:
        with pytest.raises(ValidationError):
            result = Validator.check_for_key_data_match(
                keys, parsed_data, "test")
    else:
        result = Validator.check_for_key_data_match(
            keys, parsed_data, "test")
        assert result == expected_result

def test_valid_method_check():
    # valid method
    result = Validator.validate_req_method('GET', ['GET'])
    assert result is True
    
    # valid method in quests lists
    result = Validator.validate_req_method('GET', ['GET', 'POST'])
    assert result is True
    
    # when method not allowed by quest, then raise error
    with pytest.raises(ValidationError):
        result = Validator.validate_req_method('POST', ['GET'])
    
    # when method not allowed by framework enum, then raise error
    with pytest.raises(ValidationError):
        result = Validator.validate_req_method('POST', ['PATCH'])
        
    # when method not allowed by framework enum, then raise error
    with pytest.raises(ValidationError):
        result = Validator.validate_req_method('POST', ['PATCH'])