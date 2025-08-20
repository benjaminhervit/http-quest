from app.models.base import Base
from app.extensions import db

class LastUserRequestLog(db.Model, Base):
    __tablename__ = "last_user_request_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route = db.Column(db.String(255), index=True)
    username = db.Column("username", db.String, db.ForeignKey("users.username"))
    request_json = db.Column(db.Text, nullable=False)
    response_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), index=True)