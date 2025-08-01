import pytest
from flask import Flask, request

from app.enums import QuestKey, ReqMethodType, AuthType, ParserKey
from app.game.quests_factory import make_welcome_q, make_accept_q
from app.parsers.quest_parser import QuestParser


app = Flask(__name__)

@pytest.fixture
def q1_welcome():
    return make_welcome_q()

def test_welcome_q_settings(q1_welcome):
    assert q1_welcome.is_stateless is True
    assert q1_welcome.allowed_req_methods == ReqMethodType.GET.value
    assert q1_welcome.auth_type == AuthType.NO_AUTH.value
    assert q1_welcome.execution_req_method == ReqMethodType.GET.value
    assert not q1_welcome.query_keys
    assert not q1_welcome.solution_key

@pytest.mark.parametrize("quest, keys_with_values, expected_values_per_key",
                         [
                             #  welcome q
                             (make_welcome_q(), [QuestKey.AUTH_TYPE.value,
                                                 QuestKey.METHOD_DATA.value], 
                              [AuthType.NO_AUTH.value, ['GET']]),
                             #  accept q
                             (make_accept_q(), [QuestKey.AUTH_TYPE.value,
                                                QuestKey.METHOD_DATA.value,
                                                QuestKey.QUERY_KEYS,
                                                QuestKey.ANSWER_KEY,
                                                QuestKey.ANSWER_LOC], 
                              [AuthType.NO_AUTH.value, ['GET'], ['accept'],
                               'accept', 'QUERY_DATA'])
                          ])
def test_quest_parser_on_welcome_quest(quest, keys_with_values,
                                       expected_values_per_key):
    
    settings = QuestParser.get_settings(quest)
    
    assert set(keys_with_values).issubset(set(settings.keys()))
    
    #  validate expected keys has expected value
    for i in range(len(keys_with_values)):
        key = keys_with_values[i]
        assert settings[key] == expected_values_per_key[i]
    
    #  validate that no unexpected data was parsed 
    for k, v in settings.items():
        if k not in keys_with_values:
            assert not v
    