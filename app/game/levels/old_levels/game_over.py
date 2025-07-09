from level import Level
from level_enum import LevelEnum

class GameOverLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.GAME_OVER.value, LevelEnum.GAME_OVER)
        
    def answer_is_correct(self, answer):
        return False
