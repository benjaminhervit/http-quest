from app.enums import QuestState
from app.errors import GameError

from app.game.quests.quest_data import QuestData
from app.game.quest_validator.factory import create_quest_validator


class GameManager:
    def __init__(self, quest_data:QuestData, user_answer:str, username:str):
        self.quest_data:QuestData = quest_data
        self.quest_state = QuestState.UNLOCKED
        self.quest_validator:callable = create_quest_validator(self.quest_data.quest_validator_type)
        
        self.user_answer:str = user_answer
        self.username:str = username
        
    def run_quest(self):
        self._validate_player_action()
        
    def _validate_player_action(self):
        """Check if the player has completed the quest
        """
        if self.quest_state == QuestState.UNLOCKED:
            if self.quest_validator(user_input = self.user_answer, 
                                    validation_data = self.quest_data.correct_answer):
                self.quest_state = QuestState.SUCCESSFUL_ATTEMPT
            else:
                self.quest_state = QuestState.FAILED_ATTEMPT

    def get_response(self):
        if self.quest_state == QuestState.LOCKED:
            return "Quest is still locked. Come back when you have done its pre reqs"
        if self.quest_state == QuestState.FAILED_ATTEMPT:
            return self.quest_data.response_wrong_txt
        if self.quest_state == QuestState.SUCCESSFUL_ATTEMPT:
            return f"{self.quest_data.response_correct_txt}\n {self.quest_data.next_quest_directions}"
        if self.quest_state == QuestState.COMPLETED:
            return f"{self.quest_data.response_completed_txt}"
        raise GameError(f'Could not generate response from quest state: {self.quest_state}')
    
    def get_state(self):
        return self.quest_state