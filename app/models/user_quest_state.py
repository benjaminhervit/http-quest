from sqlalchemy.orm import validates
from typing import Optional

from app.extensions import db
from app.enums import QuestState
from app.models.base import Base


class UserQuestState(db.Model, Base):
    __tablename__ = "user_quest_state"

    username = db.Column(
        db.String(255), db.ForeignKey("user.username"), primary_key=True
    )
    quest = db.Column(db.String(255), db.ForeignKey("quest.title"), primary_key=True)
    state = db.Column(db.String(255), nullable=False)

    @validates("state")
    def validate_state(self, key, value):
        # check against the saveable quest states
        valid_values = [
            QuestState.LOCKED.value,
            QuestState.UNLOCKED.value,
            QuestState.CLOSED.value,
        ]
        if value not in valid_values:
            raise ValueError(
                f"Invalided state value ({value}). allowed: {valid_values}"
            )
        return value

    @classmethod
    def update_state(cls, new_state: str, uqs: "UserQuestState"):
        uqs.state = new_state
        db.session.commit()

    # @classmethod
    # def unlock_next_quests(cls, quest: Quest, state: 'UserQuestState', username: str):
    #     if state.state == QuestState.CLOSED.value:
    #         for q in quest.next_quests:
    #             next_q_state: 'UserQuestState' = cls.get_uqs(username, q.slug)
    #             if next_q_state.state == QuestState.LOCKED.value:
    #                 cls.update_state(QuestState.UNLOCKED.value, next_q_state)

    @classmethod
    def get_state(cls, username: str, quest_title: str) -> Optional["UserQuestState"]:
        return cls.query.filter_by(username=username, quest=quest_title).first()

    def __repr__(self):
        return f'<Quest state={self.state}, slug="{self.quest}>'
