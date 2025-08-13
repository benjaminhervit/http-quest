from sqlalchemy import Integer, String, Text

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import Base
from app.enums import InputLocation, QuestExecutionStrategy, AuthType, QuestKey
from app.utils import get_clean_list_from_string, get_enum_values_as_list
from app import utils

class Quest(db.Model, Base):
    __tablename__ = "quest"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    path = db.Column(String(255), nullable=False, index=True)
    title = db.Column(String(255), nullable=False, index=True, unique=True)
    
    @classmethod
    def quest_exists(cls, title: str) -> bool:
        quest = Quest.query.filter_by(title=title).first()
        return True if quest else False