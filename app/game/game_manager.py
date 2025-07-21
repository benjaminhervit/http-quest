from app.enums import QuestState, StatusCode
from app.errors import GameError
from typing import Callable, Optional

from app.models.quest import Quest
from app.game.quest_validator.factory import create_solution_validator


class GameManager:
    def __init__(self, quest_data: Quest, user_answer: str,
                 username: str, state: str):
        
        self.quest_data: Quest = quest_data
        
        if state not in [e.value for e in QuestState]:
            raise GameError(f'quest state given to GM is not valid: {state}',
                            code=StatusCode.SERVER_ERROR)
        self.state: QuestState = QuestState(state)
        
        self.check_user_answer: Optional[Callable] = create_solution_validator(
            self.quest_data.solution_fn)

        self.user_answer: str = user_answer
        self.username: str = username

    def run_quest(self):
        if self.state == QuestState.UNLOCKED:
            if self.check_user_answer and self.check_user_answer(
                user_input=self.user_answer,
                validation_data=self.quest_data.solution):
                self.state = QuestState.COMPLETED
            else:
                self.state = QuestState.FAILED

    def get_response(self):
        if self.state == QuestState.LOCKED:
            return f"{self.quest_data.is_locked_response}"
        if self.state == QuestState.FAILED:
            return self.quest_data.failed_response
        if self.state == QuestState.COMPLETED:
            txt = self.quest_data.success_response
            new_quests: list[Quest] = self.quest_data.next_quests
            if new_quests:
                for q in new_quests:
                    path_dir = f"GET to {q.title}: {q.directions}"
                    txt += path_dir + '\n'
            return txt
        if self.state == QuestState.CLOSED:
            return f"{self.quest_data.is_completed_response}"
        raise GameError(
            f'Could not generate response from quest state: {self.state}')
    
    def get_end_state(self) -> str:
        if self.state == QuestState.COMPLETED:
            return QuestState.CLOSED.value
        elif self.state == QuestState.FAILED:
            return QuestState.UNLOCKED.value
        return self.state.value
    