from level import Level
from level_enum import LevelEnum

class GateLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_GATE.value, LevelEnum.THE_GATE)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "mellon"
            except TypeError:
                return False
        return False