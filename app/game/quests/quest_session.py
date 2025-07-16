from dataclasses import dataclass, field

from app.game.quests.quest_data import QuestData
from app.enums import QuestState, PlayerAction, StatusCode, ResponseType
from app.errors import GameError

@dataclass
class QuestSession():
    quest: QuestData
    quest_state: QuestState
    
    response_type : ResponseType = field(init=False)
    response_actions: dict[ResponseType, callable] = field(init=False)
    
    username: str
    player_answer : str | None
    player_action : PlayerAction
    player_actions: dict[PlayerAction, callable] = field(init=False)
    
    def __post_init__(self):
        self.player_actions = {
            PlayerAction.GET_QUEST: self._get_quest,
            PlayerAction.ANSWER: self.solve_quest
        }
        
        self.response_actions = {
            ResponseType.QUEST_IS_LOCKED : self._get_locked_message,
            ResponseType.GET_QUEST : self._get_quest_message,
            ResponseType.QUEST_ALREADY_COMPLETED : self._get_already_completed_message,
            ResponseType.WRONG_ANSWER : self._get_wrong_answer_message,
            ResponseType.CORRECT_ANSWER : self._get_correct_answer_message
        }
        
        self.response_type = ResponseType.QUEST_IS_LOCKED
        print(self.response_type, self.quest_state, self.player_action)
        self.set_response_type()
        print(self.response_type, self.quest_state, self.player_action)
        
    def set_response_type(self):
        if self.quest_state == QuestState.LOCKED:
            self.response_type = ResponseType.QUEST_IS_LOCKED
            
        elif self.quest_state == QuestState.COMPLETED:
            self.response_type = ResponseType.QUEST_ALREADY_COMPLETED
            
        elif self.quest_state == QuestState.UNLOCKED and self.player_action == PlayerAction.ANSWER:
            if self.player_answer == self.quest.correct_answer:
                self.response_type = ResponseType.CORRECT_ANSWER
                self.quest_state = QuestState.COMPLETED
            else:
                self.response_type = ResponseType.WRONG_ANSWER
                
        elif self.quest_state == QuestState.UNLOCKED:
            self.response_type = ResponseType.GET_QUEST
            
        else:
            raise GameError(f'Could not match quest state {self.quest_state} to any response type.', code=StatusCode.SERVER_ERROR)
    
    def get_response(self):
        response = self.response_actions.get(self.response_type)()
        if response is None:
            raise GameError(f'Could not create response for quest state {self.quest_state.value}, response type {self.response_type.value} and player action {self.player_action.value}! Ohoh!')
        return response
    
    def _get_wrong_answer_message(self) -> dict:
        msg = {
            'message' : self.quest.response_wrong_txt,
        }
        msg.update(self._get_base_message())
        return msg
        
    def _get_correct_answer_message(self) -> dict:
        msg = {
            'message' : self.quest.response_correct_txt,
            'next_quest_directions' : self.quest.next_quest.directions_txt
        }
        msg.update(self._get_base_message())
        return msg
    
    def _get_locked_message(self) -> dict:
        msg = {
            'message' : 'This quest is still locked. Stay on the route and you will get here eventually.'
        }
        return msg
    
    def _get_quest_message(self)->dict:
        msg = {
            "message" : self.quest.welcome_txt,
            "quest" : self.quest.quest_txt
        }
        msg.update(self._get_base_message())
        return msg
    
    def _get_already_completed_message(self)->dict:
        msg = {
            'message':f'You have already completed this quest dear {self.username}. Go to the next quest instead.',
            'next_quest_directions' : self.quest.next_quest.directions_txt
        }
        msg.update(self._get_base_message())
        return msg
        
    def _get_base_message(self)->dict:
        return {
            "title": self.quest.title,
            "username": self.username,
            "state": self.quest_state.value,
            "description": self.quest.description_txt
        }
    
    def _get_quest(self) ->dict:
        return {'message':'message from get_quest'}

    def solve_quest(self):
        if self.player_action == QuestState.UNLOCKED:
            correct_answer = self.quest.correct_answer.lower()
            if correct_answer is None:
                raise GameError('No correct answer in the quest settings. Some dev/designer forgot an important thingy...', code=StatusCode.SERVER_ERROR)
            
            answer = self.player_answer.lower()
            if self.player_answer is None:
                raise GameError('Found no answer for quest answer. This is some dev stuff. ', code=StatusCode.SERVER_ERROR)
            
            if answer == correct_answer:
                self.quest_state = QuestState.COMPLETED