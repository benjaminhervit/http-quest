from sqlalchemy.orm import validates
from sqlalchemy import update
from typing import Optional

from app.extensions import db
from app.enums import QuestState
from app.models.base import Base
from app.models.quest import Quest


class UserQuestState(db.Model, Base):
    __tablename__ = 'user_quest_state'
    
    username = db.Column(db.String(255), 
                         db.ForeignKey("user.username"), primary_key=True)
    path = db.Column(db.String(255),
                     db.ForeignKey("quest.path"), primary_key=True)
    state = db.Column(db.String(255), nullable=False)
    
    @validates('state')
    def validate_state(self, key, value):
        #check against the saveable quest states
        valid_values = [QuestState.LOCKED.value,
                        QuestState.UNLOCKED.value,
                        QuestState.CLOSED.value]
        if value not in valid_values:
            raise ValueError(
                f"Invalided state value ({value}). allowed: {valid_values}"
            )
        return value
    
    
    @classmethod
    def update_state(cls, new_state: str, uqs: 'UserQuestState'):
        uqs.state = new_state
        db.session.commit()
        
    @classmethod
    def unlock_next_quests(cls, quest: Quest, state: 'UserQuestState', username: str):
        if state.state == QuestState.CLOSED.value:
            for q in quest.next_quests:
                next_q_state: 'UserQuestState' = cls.get_uqs(username, q.slug)
                if next_q_state.state == QuestState.LOCKED.value:
                    cls.update_state(QuestState.UNLOCKED.value, next_q_state)

    @classmethod
    def get_uqs(cls, username: str, slug: str) -> Optional['UserQuestState']:
        return cls.query.filter_by(
            username=username,
            slug=slug
            ).first()
        
    def __repr__(self):
        return (f'<Quest state={self.state}, '
                f'slug="{self.slug}>')