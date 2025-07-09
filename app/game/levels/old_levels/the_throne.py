from level import Level
from level_enum import LevelEnum

class ThroneLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_THRONE_ROOM.value, LevelEnum.THE_THRONE_ROOM)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == "jason where is the crown"
            except TypeError:
                return False
        return False