from sqlalchemy import Integer, String

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import Base

class Quest(db.Model, Base):
    __tablename__ = "quest"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    title = db.Column(String(255), nullable=False, index=True, unique=True)
    
    @classmethod
    def quest_exists(cls, title: str) -> bool:
        quest = Quest.query.filter_by(title=title).first()
        return True if quest else False