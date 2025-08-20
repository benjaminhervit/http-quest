from sqlalchemy import Integer, String, Boolean, update, func, select
from sqlalchemy.orm import validates
from typing import Optional

from app.extensions import db
from app.enums import QuestState
from app.models.base import Base
from app.models import User, Quest


class UserQuestState(db.Model, Base):
    __tablename__ = "user_quest_state"
    
    id = db.Column("id", Integer, autoincrement=True)
    username = db.Column("username",
        String, db.ForeignKey("users.username"), primary_key=True
    )
    quest = db.Column("quest", String, db.ForeignKey("quest.title"), primary_key=True)
    state = db.Column("state", String, nullable=False)
    xp_awarded = db.Column("xp_awarded", Boolean, nullable=False, default=False)

    @validates("state")
    def validate_state(self, key, value):
        # check against the saveable quest states
        valid_values = [
            QuestState.LOCKED.value,
            QuestState.UNLOCKED.value,
            QuestState.CLOSED.value,
            QuestState.COMPLETED.value,
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

    @classmethod
    def get_state(cls, username: str, quest_title: str) -> Optional["UserQuestState"]:
        return cls.query.filter_by(username=username, quest=quest_title).first()

    def __repr__(self):
        return f'<Quest state={self.state}, slug="{self.quest}>'

    @classmethod
    def complete_and_award_xp(cls, username: str, quest_title: str) -> bool:
        print("TIME TO GET SOME XP!")
        print(username, quest_title)
        uqs = UserQuestState.__table__
        users = User.__table__
        quests = Quest.__table__
        
        res = db.session.execute(
            update(uqs)
            .where(uqs.c.username == username, uqs.c.quest == quest_title)
            .where((uqs.c.xp_awarded.is_(False)) | (uqs.c.xp_awarded.is_(None)))
            .values(state=QuestState.COMPLETED.value, xp_awarded=True)
        )
        
        print(f"res: {res}")
        print(f"res.rowcount: {res.rowcount}")
        
        if res.rowcount != 1:
            db.session.commit()
            return False #No XP
        
        quest_xp = db.session.execute(
            select(quests.c.xp).where(quests.c.title==quest_title)
            ).scalar_one_or_none() or 0
        
        if quest_xp:
            db.session.execute(
                update(users)
                .where(users.c.username == username)
                .values(xp=func.coalesce(users.c.xp, 0) + quest_xp)
            )
        
        db.session.commit()
        return True