from app.enums import QuestState
from app.errors import GameError

from app.game.quests.quest_data import QuestData
from app.game.quests.quest_validator.factory import create_quest_validator


class GameManager:
    def __init__(self, quest_data:QuestData, user_inputs:dict, username:str):
        self.quest_data = quest_data
        self.quest_state = QuestState.LOCKED
        self.quest_validator = create_quest_validator(self.quest_data.quest_validator_type)
        
        self.user_inputs = user_inputs
        self.username = username
        
    def run_quest(self):
        self._validate_player_action()
        response = self._get_response()
        self._reset()
        return response
        
    def _validate_player_action(self):
        if self.quest_state == QuestState.UNLOCKED:
            if self.quest_validator(user_inputs = self.user_inputs):
                self.quest_state = QuestState.COMPLETED
        
    def _get_response(self):
        if self.quest_state == QuestState.LOCKED:
            return "Quest is still locked. Come back when you have done its pre reqs"
        if self.quest_state == QuestState.FAILED_ATTEMPT:
            return "Sorry, that was the wrong answer. Try again."
        if self.quest_state == QuestState.SUCCESSFUL_ATTEMPT:
            return "WOHO! YOU DID IT! ONWARDS!"
        if self.quest_state == QuestState.COMPLETED:
            return "You already completed this quest! What are you even doing here?? Get going! I believe in you!"
        raise GameError(f'Could not generate response from quest state: {self.quest_state}')
    
    def _reset(self):
        if self.quest_state != QuestState.LOCKED or self.quest_state != QuestState.COMPLETED:
            self.quest_state = QuestState.UNLOCKED
        #update state in db when model is imported