from typing import Callable, Optional

from app.enums import QuestState, StatusCode, ParserKey
from app.errors import GameError
from app.models import Quest, User
from app.game.gm_execute_strategy.factory import create_gm_execute_strategy


class GameManager:
    def __init__(self, quest_data: Quest,
                 input_data: dict,
                 player_profile: User | None = None,
                 state: QuestState | None = None):

        # quest data
        self.quest_data: Quest = quest_data

        # check if request method indicates execution of informative
        self.execute = (input_data.get(ParserKey.METHOD_DATA) ==
                        self.quest_data.execution_req_method)
        
        # get execution function
        # TODO: Consider moving it to run_quest() instead
        self.execute_strategy: Callable = create_gm_execute_strategy(
            self.quest_data.execution_strategy)
        
        # inputs used in execution mode
        self.player_inputs = input_data.get(ParserKey.INPUT_DATA)
        
        # set state dependning on quest and player settings
        if not quest_data.is_stateless and state is None:
            raise GameError(f'Quest state is None but Quest is not stateless.'
                            f'Quest:{quest_data.title}. is_stateless:'
                            f'{quest_data.is_stateless}')
        
        self.state = state
        if quest_data.is_stateless:
            self.state = QuestState.UNLOCKED
        
        if not isinstance(self.state, QuestState):
            raise GameError('Quest state failed to be set correctly.\n'
                            f'Quest: {quest_data.title}\n'
                            f'state: {state}\n'
                            f'profile: {player_profile}\n'
                            f'input: {input_data}\n')

        # player data
        self.user_name = "Stranger"
        if player_profile:
            self.user_name = player_profile.username
            
        # responses
        self.response_actions = {
            QuestState.LOCKED: lambda: self.quest_data.is_locked_response,
            QuestState.UNLOCKED: self._get_welcome_response,
            QuestState.FAILED: self._get_failed_attempt_response,
            QuestState.COMPLETED: self._get_completed_response,
            QuestState.CLOSED: lambda: self.quest_data.is_completed_response
        }

    def run_quest(self):
        self.execute_strategy(self)

    def get_response(self):
        response_action = self.response_actions.get(self.state)
        if response_action is None:
            raise GameError(
                f'No response action found for quest state: {self.state}')
        
        response = response_action()
        if not response:
            raise GameError(
                f'Could not generate response from quest state: {self.state}')
        
        return response
    
    def _get_welcome_response(self):
        return self._get_base_story()
    
    def _get_completed_response(self):
        response = self._get_base_story()
        response.update({'story': self.quest_data.success_response})
        next_quests_dir = [
            {'directions': nq.directions, 'title': nq.title}
            for nq in getattr(self.quest_data, 'next_quests', [])
        ]
        response.update({'unlocked_quests': next_quests_dir})
        return response
    
    def _get_failed_attempt_response(self):
        response = self._get_base_story()
        response.update({'story': self.quest_data.failed_response})
        return response
    
    def _get_base_story(self):
        return {
            'title': self.quest_data.title,
            'story': self.quest_data.story,
            'quest': self.quest_data.quest_description,
            'directions': self.quest_data.directions
        }
    
    def get_end_state(self) -> str:
        if self.state == QuestState.COMPLETED:
            return QuestState.CLOSED.value
        elif self.state == QuestState.FAILED:
            return QuestState.UNLOCKED.value
        return self.state.value
    
    def set_state(self, new_state: QuestState):
        self.state = new_state