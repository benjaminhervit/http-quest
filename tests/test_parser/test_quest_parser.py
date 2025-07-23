"""
Unit testing of the parsing strategies.
The testing relies on flasks test_request_context.
Strategies implement some extra rules just to be sure that
some standard rules, e.g. no Form together with GET.
"""

import pytest

from app.enums import ParserKey, AuthType
from app.models.quest import Quest
from app.parsers import QuestParser
from app.game.quests.null_q import null_Q

@pytest.fixture
def null_quest() -> Quest:
    return null_Q

@pytest.mark.parametrize(
    "quest,valid_keys",
    [(null_Q, [ParserKey.METHOD_DATA, ParserKey.AUTH_TYPE])]
)
def test_get_only_expected_settings(quest, valid_keys):
    parsed = QuestParser.get_settings(quest)
    for k, v in parsed.items():
        if k in valid_keys:
            assert v is not None
        else:
            assert not v

def test_parser_get_auth(null_quest: Quest):
    parsed = QuestParser.get_settings(null_quest)
    assert parsed.get(ParserKey.AUTH_TYPE) == AuthType.NO_AUTH

def test_quest_parser_method_is_get(null_quest: Quest):
    parsed = QuestParser.get_settings(null_quest)
    method_keys = parsed.get(ParserKey.METHOD_DATA)
    assert method_keys == ['GET']