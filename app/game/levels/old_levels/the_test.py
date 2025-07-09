from level import Level
from level_enum import LevelEnum

class TestLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_TEST.value, LevelEnum.THE_TEST)
        
    def answer_is_correct(self, answer):
        try:
            answer = int(answer)
            success = answer == 42
            return success
        except TypeError:
            return False