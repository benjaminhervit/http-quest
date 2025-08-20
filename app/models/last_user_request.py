from typing import Any
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.models.base import Base
from app.extensions import db
from app.utils import validate_utils


class LastUserRequestLog(db.Model, Base):
    __tablename__ = "last_user_request_log"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    route = db.Column("route", db.String(255), nullable=False)
    username = db.Column(
        "username",
        db.String(80),
        db.ForeignKey("users.username", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        unique=True, 
        index=True,
    )
    request_json = db.Column("request_json", db.Text, nullable=False)
    response_json = db.Column("response_json", db.Text, nullable=False)
    created_at = db.Column("created_at", db.DateTime, server_default=db.func.now(), index=True, nullable=False)
    updated_at = db.Column("updated_at", db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)
    
    @classmethod
    def upsert_for_username(cls, *, username: str, route: str, request_json: str, response_json: str) -> 'LastUserRequestLog':
        
        statement = sqlite_insert(cls).values(
            username=username,
            route=route,
            request_json=request_json,
            response_json=response_json,
        ).on_conflict_do_update(
            index_elements=[cls.username],
            set_={
                "route": route,
                "request_json": request_json,
                "response_json": response_json,
                "updated_at": db.func.now()
            },
        )
        
        db.session.execute(statement)
        db.session.commit()
        return cls.query.filter_by(username=username).first()