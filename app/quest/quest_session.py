from dataclasses import dataclass, field
from app.quest import Serializable
from app.models import UserQuestState
from app.enums import QuestState


@dataclass
class QuestSession(Serializable):
    quest_title: str
    state: str = field(init=False)
    username: str

    def __post_init__(self):
        self.state = QuestState.LOCKED.value
        state_obj: UserQuestState | None = UserQuestState.get_state(
            self.username, self.quest_title
        )
        if state_obj:
            self.state = state_obj.state
