from app.enums import QuestState
from app.errors import GameError
from typing import Callable, Optional

from app.game.quests.quest_data import QuestData
from app.models.quest import Quest
from app.game.quest_validator.factory import create_solution_validator


class GameManager:
    def __init__(self, quest_data: Quest, user_answer: str, username: str):
        self.quest_data: Quest = quest_data
        self.quest_state: QuestState = QuestState.UNLOCKED
        self.check_user_answer: Optional[Callable] = create_solution_validator(
            self.quest_data.solution_fn
            )

        self.user_answer: str = user_answer
        self.username: str = username

    def run_quest(self):
        if self.quest_state == QuestState.UNLOCKED:
            if self.check_user_answer and self.check_user_answer(
                user_input=self.user_answer,
                validation_data=self.quest_data.solution):
                self.quest_state = QuestState.SUCCESSFUL_ATTEMPT
            else:
                self.quest_state = QuestState.FAILED_ATTEMPT

    def get_response(self):
        if self.quest_state == QuestState.LOCKED:
            return f"{self.quest_data.is_locked_response}"
        if self.quest_state == QuestState.FAILED_ATTEMPT:
            return self.quest_data.failed_response
        if self.quest_state == QuestState.SUCCESSFUL_ATTEMPT:
            next_direction = (
                self.quest_data.next_quest.directions
                if self.quest_data.next_quest else '')
            return (
                f"{self.quest_data.success_response}\n "
                f"{next_direction}"
            )
        if self.quest_state == QuestState.COMPLETED:
            return f"{self.quest_data.is_completed_response}"
        raise GameError(
            f'Could not generate response from quest state: {self.quest_state}'
            )
    
    def get_state(self):
        return self.quest_state
    