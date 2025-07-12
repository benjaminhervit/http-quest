from app.game.enums.game_state import GameState
from app.models.quest import Quest as QM

class Quest:
    quest_model = QM
    def __init__(self, title:str, description:str, quest:str, correct_answer:str, completed_message:str, fail_message:str, status:GameState=GameState.LOCKED):
        self.title = title
        self.description = description
        self.quest = quest
        self.correct_answer = correct_answer
        self.completed_message = completed_message
        self.fail_message = fail_message
        self.status = status
        
        self.json = {
            "title": self.title,
            "description": self.description,
            "quest": self.quest,
            "correct_answer": self.correct_answer,
            "completed_message": self.completed_message,
            "fail_message": self.fail_message,
            "status": self.status.name if hasattr(self.status, "name") else str(self.status)
        }
    
    def set_status(self, new_status:GameState) -> GameState:
        if self.status != GameState.LOCKED and new_status == GameState.LOCKED:
            return GameState.QUEST_NOT_RELOCKABLE
        self.status = new_status
        return GameState.OK