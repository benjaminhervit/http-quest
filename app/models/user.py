from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.sql import func

from app.enums import QuestTitle
from app.extensions import db
from app.models.base import Base
from app.errors import ValidationError, QuestError


class User(db.Model, Base):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(31), nullable=False, unique=True)
    xp = db.Column("xp", db.Integer, nullable=False, default=0) 

    start_quest = db.Column(QuestTitle.START_QUEST.value, String(255), nullable=False, default="locked")  # handlers are ignoring this for this quest

    register_quest = db.Column(QuestTitle.REGISTER_QUEST.value, String(255), nullable=False, default="locked")  # handlers are ignoring this for this quest

    identify_quest = db.Column(QuestTitle.IDENTIFY_QUEST.value, String(255), nullable=False, default="locked")

    jason_quest = db.Column(QuestTitle.JASON_QUEST.value, String(255), nullable=False, default="locked")

    wall_quest = db.Column(QuestTitle.WALL_QUEST.value, String(255), nullable=False, default="locked")
    wall_counter = db.Column(QuestTitle.WALL_QUEST.value+"_counter", db.Integer, nullable=False, default=0)
    wall_last_req_at = db.Column(DateTime, server_default=func.now())

    git_monster_quest = db.Column(QuestTitle.GIT_MONSTER_QUEST.value, String(255), nullable=False, default="locked")

    the_crown_quest = db.Column(QuestTitle.THE_CROWN_QUEST.value, String(255), nullable=False, default="locked")

    # GET ALL
    @classmethod
    def get_all(cls):
        return User.query.all()

    @classmethod
    def get_all_ordered_by_xp(cls):
        return User.query.order_by(User.xp.desc()).all()

    # GET USER
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def user_exists(cls, username) -> bool:
        user = cls.get_by_username(username)
        return True if user else False

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    
    # QUEST STATES
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
    
    # WALL QUEST API
    @classmethod
    def update_wall_counter(cls, username: str, delta_val: int) -> int:
        user = cls.get_by_username(username)
        if not user:
            raise ValidationError(f"Could not find user {username} in db.")
        user.wall_counter += delta_val
        db.session.commit()
        return user.wall_counter
    
    @classmethod
    def reset_wall_counter(cls, username: str) -> int:
        user = cls.get_by_username(username)
        if not user:
            raise ValidationError(f"Could not find user {username} in db.")
        user.wall_counter += 0
        db.session.commit()
        return user.wall_counter
    
    @classmethod
    def get_wall_last_req_at(cls, username: str):
        user = cls.get_by_username(username)
        if not user:
            raise ValidationError(f"Could not find user {username} in db.")
        return user.wall_last_req_at
    
    @classmethod
    def update_wall_last_req_at(cls, username: str) -> DateTime:
        user = cls.get_by_username(username)
        if not user:
            raise ValidationError(f"Could not find user {username} in db.")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        user.wall_last_req_at = now
        db.session.commit()
        return now
        
    
    @classmethod
    def get_wall_counter(cls, username: str) -> int:
        user = cls.get_by_username(username)
        if not user:
            raise ValidationError(f"Could not find user {username} in db.")
        return user.wall_counter
        #return getattr(user, QuestTitle.BEG_QUEST.value+"_counter", None)
    
    # XP
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

    def __repr__(self):
        return f"<User {self.id}, {self.username}>"

    def to_dict(self):
        return {"id": self.id, "username": self.username, "xp": self.xp}
