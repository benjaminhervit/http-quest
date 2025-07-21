from sqlalchemy import Integer, String, Text
from slugify import slugify
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import Base
from app.enums import InputLocation, ReqMethodType

class Quest(db.Model, Base):
    __tablename__ = "quest"
    
    #route and identifier
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    slug = db.Column(String(255), nullable=False, index=True)
    
    #content
    title = db.Column(String(255), nullable=False, index=True)
    directions = db.Column(Text, nullable=False)
    story = db.Column(Text, nullable=False)
    success_response = db.Column(Text, nullable=False)
    failed_response = db.Column(Text, nullable=False)
    is_locked_response = db.Column(Text, nullable=False)
    is_completed_response = db.Column(Text, nullable=False)
    
    #solution related
    quest = db.Column(Text, nullable=True)
    expected_solution = db.Column(Text, nullable=True)
    solution_fn = db.Column(String(255), nullable=True)
    
    #relationships
    prev_quest_id = db.Column(
        db.Integer,
        db.ForeignKey("quest.id"),
        nullable=True)

    prev_quests = db.relationship(
        "Quest",
        remote_side=[id],
        backref="next_quests")

    # parsing settings - all can be null if the setting is not needed.
    # TODO: Consider explicit "NONE" to minimize errors and enum comparison
    allowed_req_methods = db.Column(String(255), nullable=True)
    query_keys = db.Column(String(255), nullable=True)
    json_keys = db.Column(String(255), nullable=True)
    form_keys = db.Column(String(255), nullable=True)
    headers_keys = db.Column(String(255), nullable=True)
    
    username_loc = db.Column(String(255), nullable=True)
    token_loc = db.Column(String(255), nullable=True)
    input_loc = db.Column(String(255), nullable=True)
    answer_key = db.Column(String(255), nullable=True)
    auth_type = db.Column(String(255), nullable=True)
    
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
    
    @classmethod
    def get_by_slug(cls, slug: str):
        return cls.query.filter_by(slug=slug).first()

    def __repr__(self):
        return (f'<Quest id={self.id}, '
                f'title="{self.title}>')

    
    @validates('username_loc', 'token_loc', 'answer_loc')
    def validate_input_location(self, key, value):
        #check against the saveable quest states
        valid_values = [e.value for e in InputLocation]
        if value not in valid_values:
            raise ValueError(
                f"Invalided input locatoin value ({value}). allowed: {valid_values}"
            )
        return value
    
    @validates('allowed_req_methods')
    def validate_allowed_methods(self, key, value: str):
        #  check against the saveable quest states
        if value is None:
            raise ValueError(
                f"Must have at least GET method. allowed: {valid_values}"
            )
        
        valid_values = [e.value for e in ReqMethodType]
        value = value.replace(' ', '').strip()  # removing empty spaces
        methods: list[str] = value.split(',')
        methods = [m.strip() for m in methods if m]
        if methods == []:
            raise ValueError(
                f"No methos after cleaning {value}. allowed: {valid_values}"
            )
        
        for method in methods:
            if method not in valid_values:
                raise ValueError(
                    f"Invalided input locatoin value ({value}). allowed: {valid_values}"
                )
        return value
    
    @validates('query_keys', 'json_keys', 'form_keys', 'header_keys')
    def validate_expected_keys(self, key, value: str):
        if value is not None and ' ' in value:
            raise ValueError(
                f"No white spaces in keys. Use comma , as separator _ for key_name_spaces. Error found in: {value}"
                )
        return value