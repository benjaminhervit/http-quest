import pytest
from app.game.game_manager import GameManager
from app.game.quests.welcome import welcome_Q
from app.enums import QuestState, ParserKey

def test_unlocked_welcome():
    parsed: dict = {ParserKey.METHOD_DATA: 'GET'}
    GM = GameManager(quest_data=welcome_Q,
                     req_data=parsed,
                     state=QuestState.UNLOCKED)
    
    assert GM.state == QuestState.UNLOCKED
    GM.run_quest()
    assert GM.state == QuestState.COMPLETED

def test_unlocked_welcom_completes_automatically():
    parsed: dict = {ParserKey.METHOD_DATA: 'GET'}
    GM = GameManager(quest_data=welcome_Q,
                     req_data=parsed,
                     state=QuestState.UNLOCKED)
    
    assert GM.state == QuestState.LOCKED
    assert not GM.user_answer
    assert not GM.username
    
    GM = GameManager(quest_data=welcome_Q,
                     req_data=parsed,
                     state=QuestState.LOCKED)
    
    assert GM.state == QuestState.LOCKED
    assert not GM.user_answer
    assert not GM.username
    
    response = GM.get_response()
    assert response == GM.quest_data.is_locked_response
    
    GM.run_quest()
    response = GM.get_response()
    assert response == GM.quest_data.is_locked_response
