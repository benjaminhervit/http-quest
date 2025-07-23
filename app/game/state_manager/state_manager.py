from typing import Callable

from app.models import Quest, User
from app.enums import QuestState

class StateManager:
    def __init__(self, set_start_strategy: Callable,
                 end_start_strategy: Callable,
                 update_state_db_strategy: Callable) -> None:
        
        self.start_state_strategy: Callable = set_start_strategy
        self.end_state_strategy: Callable = end_start_strategy
        self.update_state_db_strategy: Callable = update_state_db_strategy
    
    def get_start_state(self, quest: Quest, user: User | None) -> QuestState:
        return self.start_state_strategy(quest, user)
    
    def get_end_state(self, state) -> QuestState:
        return self.end_state_strategy(state)
    
    def update_quest_state(self, new_state: str, username: str,
                           slug: str) -> bool:
        return self.update_state_db_strategy(new_state, username, slug)
