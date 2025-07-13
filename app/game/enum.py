from enum import Enum

class GameEnum(Enum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    QUEST_NOT_RELOCKABLE = "CANNOT_RELOCK_QUEST"
    OK = "OK"