from app.authenticator.factory import create_authenticator
from app.enums import QuestKey, ParserKey, AuthType
from app.errors import AuthenticationError

import pytest

def test_value_at_expected_username_location():
    #when settings defines username loc, then settings has expected data on that location
    settings = {QuestKey.USERNAME_LOC:ParserKey.QUERY_DATA}
    parsed_data = {ParserKey.QUERY_DATA:'test'}
    auth = create_authenticator(AuthType.NO_AUTH)
    identity = auth.get_identity(parsed_data, settings)
    assert identity.get(ParserKey.USERNAME) == 'test'
    
    
def test_error_when_data_is_missing_username():
    settings = {QuestKey.USERNAME_LOC: ParserKey.QUERY_DATA}
    parsed_data = {ParserKey.METHOD_DATA: 'test'}
    auth = create_authenticator(AuthType.NO_AUTH)
    
    
    with pytest.raises(AuthenticationError):
        identity = auth.get_identity(parsed_data, settings)
        
def test_empty_when_no_username_expected():
    settings = {}
    parsed_data = {ParserKey.QUERY_DATA: 'username'}
    auth = create_authenticator(AuthType.NO_AUTH)
    identity = auth.get_identity(parsed_data, settings)
    
    assert not identity.get(ParserKey.USERNAME) 