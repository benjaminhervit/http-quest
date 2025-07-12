from enum import Enum

class GameState(Enum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    QUEST_NOT_RELOCKABLE = "CANNOT_RELOCK_QUEST"
    OK = "OK"