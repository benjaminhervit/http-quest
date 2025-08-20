from app.extensions import db
from app.models.base import Base


class User(db.Model, Base):
    __tablename__ = "users"
    
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(31), nullable=False, unique=True)
    xp = db.Column("xp", db.Integer, nullable=False, default=0)

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
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    def __repr__(self):
        return f"<User {self.id}, {self.username}>"

    def to_dict(self):
        return {"id": self.id, "username": self.username, "xp": self.xp}
