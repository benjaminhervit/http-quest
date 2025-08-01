"""
    ## class: `STATE MANAGER`
| ID     |  | Test Description                                                                 |
|--------|--|-----------------------------------------------------------------------------------|
| SM-001 |[x]| when quest is stateless, then start state COMPLETED                              |
| SM-001 |[ ]| when quest has state, and user has not reached the quest, then the state is LOCKED                     |
| SM-001 |[ ]| when the quest has state, and the user has reached the quest, then the initial state is UNLOCKED    |
| SM-001 |[ ]| when the quest has state and is UNLOCKED, when the user completes the quest, the state changes to COMPLETED  |
| SM-001 |[ ]| when the quest has state and is UNLOCKED, when the user fails the quest, the state changes to FAILED.     |
| SM-001 |[ ]| when the quest has state and is COMPLETED, then the end state is CLOSED.      |
| SM-001 |[ ]| when the quest has state and is FAILED, then the end state is reset to UNLOCKED.   |
| SM-001 |[x]| when state is not a valid QuestState enum, then State Manager raises an error.     |
"""


import pytest
from flask import Flask, request

from app.enums import QuestState
from app.errors import GameError
from app.game.quests_factory import make_welcome_q, make_accept_q, make_null_q
from app.game.state_manager.state_manager import StateManager
from app.game.state_manager.factory import create_state_manager
import app.game.state_manager.strategies.start_session_strategies as start_state_strategies
import app.game.state_manager.strategies.end_session_strategies as end_state_strategies

@pytest.fixture
def q1_welcome():
    return make_welcome_q()

@pytest.fixture
def null_quest():
    return make_null_q()

# @pytest.mark.parametrize("",[()])
def test_stateless_starts_as_completed(null_quest):
    #. unit test of strategy
    with pytest.raises(ValueError):
        state = start_state_strategies.get_stateless_start('123', None)
    
    assert start_state_strategies.get_stateless_start(null_quest, None) == QuestState.COMPLETED
    
    # integration test with state manager
    sm = create_state_manager(True)
    assert sm.get_start_state(null_quest, None) == QuestState.COMPLETED
    
def test_invalid_state_throws_error():
    with pytest.raises(ValueError) as exc:
        end_State = end_state_strategies.set_by_active_state('123')
        
def test_correct_end_state():
    #when given state is wrong, then throw a value error
    with pytest.raises(ValueError) as exc:
        end_State = end_state_strategies.set_by_active_state(123)
        

