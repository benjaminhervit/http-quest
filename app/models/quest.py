from app.extensions import db
from sqlalchemy import Integer, String, Text
from slugify import slugify
from sqlalchemy.inspection import inspect

class Quest(db.Model):
    __tablename__ = "quest"
    
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    title = db.Column(String(255), nullable=False, index=True)
    slug = db.Column(String(255), nullable=False, index=True)
    directions = db.Column(Text, nullable=False)
    story = db.Column(Text, nullable=False)
    quest = db.Column(Text, nullable=False)
    success_response = db.Column(Text, nullable=False)
    failed_response = db.Column(Text, nullable=False)
    is_locked_response = db.Column(Text, nullable=False)
    is_completed_response = db.Column(Text, nullable=False)
    solution = db.Column(Text, nullable=True)
    solution_fn = db.Column(String(255), nullable=False)

    next_quest_id = db.Column(
        db.Integer,
        db.ForeignKey("quest.id"),
        nullable=True)

    next_quest = db.relationship(
        "Quest",
        remote_side=[id],
        backref="previous_quests")

    req_method = db.Column(String(10), nullable=False, index=True)
    username_loc = db.Column(String(255), nullable=False)
    token_loc = db.Column(String(255), nullable=False)
    answer_loc = db.Column(String(255), nullable=False)
    answer_key = db.Column(String(255), nullable=False)
    auth_type = db.Column(String(255), nullable=False)
    
    def __init__(self, title, **kwargs):
        self.title = title
        self.slug = slugify(title)
        super().__init__(**kwargs)
        
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in inspect(self.__class__).columns}
    
    def print_all_fields(self):
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.name)
            print(f"{column.name} = {value}")
        
    @classmethod
    def get_by_id(cls, quest_id):
        return cls.query.get(quest_id)

    def __repr__(self):
        return f'<Quest id={self.id}, title="{self.title}", method="{self.req_method}">'
