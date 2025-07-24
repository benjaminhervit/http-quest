from typing import Callable, Optional

from app.enums import QuestState, StatusCode, ParserKey
from app.errors import GameError
from app.models import Quest, User
from app.game.game_manager.factory import create_gm_execute_strategy
from app.request_manager.request_context import RequestContext


class QuestManager:
    def __init__(self, context: RequestContext):

        # quest data
        self.quest: Quest = context.quest
        self.req_method = context.parsed.get(ParserKey.METHOD_DATA)
        self.player_inputs: dict = context.parsed
        self.user: User | None = context.user
        
        if context.state not in QuestState:
            raise GameError(f'GM received invalid state: {context.state}',
                            code=StatusCode.SERVER_ERROR)
        self.state: QuestState = QuestState(context.state)

        # check if request method indicates execution of informative
        self.execute = (self.req_method == self.quest.execution_req_method)
        
        # get execution function
        # TODO: Consider moving it to run_quest() instead
        self.execute_strategy: Callable = create_gm_execute_strategy(
            self.quest.execution_strategy)
            
        # responses
        self.response_actions = {
            QuestState.LOCKED: lambda: self.quest.is_locked_response,
            QuestState.UNLOCKED: self._get_welcome_response,
            QuestState.FAILED: self._get_failed_attempt_response,
            QuestState.COMPLETED: self._get_completed_response,
            QuestState.CLOSED: lambda: self.quest.is_completed_response
        }

    def run(self):
        if self.state == QuestState.UNLOCKED and self.execute:
            self.set_state(QuestState.FAILED)
            if self.execute_strategy(self):
                self.set_state(QuestState.COMPLETED)

    def get_response(self):
        response_action = self.response_actions.get(QuestState(self.state))
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
        response.update({'story': self.quest.success_response})
        next_quests_dir = [
            {'directions': nq.directions, 'title': nq.title}
            for nq in getattr(self.quest, 'next_quests', [])
        ]
        response.update({'unlocked_quests': next_quests_dir})
        return response
    
    def _get_failed_attempt_response(self):
        response = self._get_base_story()
        response.update({'story': self.quest.failed_response})
        return response
    
    def _get_base_story(self):
        return {
            'title': self.quest.title,
            'story': self.quest.story,
            'quest': self.quest.quest_description,
            'directions': self.quest.directions
        }
    
    def set_state(self, new_state: QuestState):
        self.state = new_state