from sqlalchemy import Integer, String


from app.extensions import db
from app.models.base import Base


class Quest(db.Model, Base):
    __tablename__ = "quest"
    id = db.Column("id", Integer, primary_key=True, autoincrement=True)
    title = db.Column("title", String(255), nullable=False, index=True, unique=True)
    xp = db.Column("xp", db.Integer, nullable=False, default=0)

    @classmethod
    def quest_exists(cls, title: str) -> bool:
        quest = Quest.query.filter_by(title=title).first()
        return True if quest else False
