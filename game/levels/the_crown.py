from level import Level
from level_enum import LevelEnum

class CrownLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_CROWN.value, LevelEnum.THE_CROWN)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == "give me my new cool hat jason"
            except TypeError:
                return False
        return False