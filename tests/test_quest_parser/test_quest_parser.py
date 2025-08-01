"""
Unit testing of the parsing strategies.
The testing relies on flasks test_request_context.
Strategies implement some extra rules just to be sure that
some standard rules, e.g. no Form together with GET.
"""

import pytest

from app.enums import QuestKey, QuestExecutionStrategy
from app.models.quest import Quest
from app.parsers import QuestParser
from app.game.quests_factory.make_null_q import make_null_q

@pytest.fixture
def null_quest() -> Quest:
    return make_null_q()

@pytest.fixture
def wrong_quest() -> Quest:
    return Quest(
            # content
            title="",
            story="",
            directions="",
            quest_description="",

            # parsing
            allowed_req_methods="GET",

            # authentication
            auth_type='NOT GOOD',

            # execution
            is_stateless=True,
            execution_strategy=QuestExecutionStrategy.AUTO_COMPLETE.value,
            execution_req_method="GET"
    )

def test_min_key_requirements(null_quest):
    settings = QuestParser.get_settings(null_quest)
    keys = settings.keys()
    assert len(keys) == 6
    assert set(keys).issubset(set({QuestKey.METHOD_DATA.value, 
                                   QuestKey.AUTH_TYPE.value,
                                   QuestKey.QUERY_KEYS,
                                   QuestKey.ANSWER_KEY,
                                   QuestKey.ANSWER_LOC,
                                   QuestKey.FORM_KEYS
                                   }))
    
    for k in keys:
        assert QuestKey(k)