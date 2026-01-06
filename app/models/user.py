from sqlalchemy import String

from app.enums import QuestTitle
from app.extensions import db
from app.models.base import Base

class User(db.Model, Base):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(31), nullable=False, unique=True)
    xp = db.Column("xp", db.Integer, nullable=False, default=0) 
    start_quest = db.Column(QuestTitle.START_QUEST.value, String(255), nullable=False, default="locked")  # handlers are ignoring this for this quest
    register_quest = db.Column(QuestTitle.REGISTER_QUEST.value, String(255), nullable=False, default="locked")  # handlers are ignoring this for this quest
    identify_quest = db.Column(QuestTitle.IDENTIFY_QUEST.value, String(255), nullable=False, default="locked")
    jason_quest = db.Column(QuestTitle.JASON_QUEST.value, String(255), nullable=False, default="locked")

    @classmethod
    def get_all(cls):
        return User.query.all()

    @classmethod
    def user_exists(cls, username) -> bool:
        user = cls.get_by_username(username)
        return True if user else False

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_user_quest_State(cls, username: str, quest: str) -> str:
        user = cls.get_by_username(username)
        if user:
            return getattr(user, quest, None)
        return None
    
    @classmethod
    def update_quest_state(cls, username: str, quest: str, new_state: str) -> bool:
        user = cls.get_by_username(username)
        if user:
            if hasattr(user, quest):
                setattr(user, quest, new_state)
                db.session.commit()
                return True
        return False
    
    @classmethod
    def update_xp(cls, username: str, delta_xp: int) -> int:
        user = cls.get_by_username(username)
        if user:
            if hasattr(user, "xp"):
                current_xp = getattr(user, "xp", None)
                setattr(user, "xp", current_xp + delta_xp)
                db.session.commit()
                return getattr(user, "xp", None)
        return -1

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    def __repr__(self):
        return f"<User {self.id}, {self.username}>"

    def to_dict(self):
        return {"id": self.id, "username": self.username, "xp": self.xp}
