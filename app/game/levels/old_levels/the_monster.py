from level import Level
from level_enum import LevelEnum

class GitLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_MONSTER.value, LevelEnum.THE_MONSTER)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "pull/add/commit/push"
            except TypeError:
                return False
        return False