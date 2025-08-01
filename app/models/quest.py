from sqlalchemy import Integer, String, Text
from slugify import slugify
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import Base
from app.enums import InputLocation, QuestExecutionStrategy, AuthType, QuestKey
from app.utils import get_clean_list_from_string, get_enum_values_as_list
from app import utils

class Quest(db.Model, Base):
    __tablename__ = "quest"
    
    # route and identifier
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    slug = db.Column(String(255), nullable=False, index=True)
    
    # content
    title = db.Column(String(255), nullable=False, index=True)
    directions = db.Column(Text, nullable=False)
    story = db.Column(Text, nullable=False)
    quest_description = db.Column(Text, nullable=True)
    success_response = db.Column(Text, nullable=False)
    failed_response = db.Column(Text, nullable=False)
    is_locked_response = db.Column(Text, nullable=False)
    is_completed_response = db.Column(Text, nullable=False)
    
    # request settings
    allowed_req_methods = db.Column(String(255), nullable=False)
    query_keys = db.Column(String(255), nullable=True)
    form_keys = db.Column(String(255), nullable=True)
    
    # TODO: uncomment with first json quest
    # expects_json = db.Column(db.Boolean, nullable=False)
    # json_keys = db.Column(String(255), nullable=True)
    
    # TODO: uncomment with first form quest
    # expects_form = db.Column(db.Boolean, nullable=False)
    # form_keys = db.Column(String(255), nullable=True)
    
    # TODO: uncomment with first headers quest
    # expects_headers = db.Column(db.Boolean, nullable=False)
    # headers_keys = db.Column(String(255), nullable=True)
    
    # TODO: uncommment with first username quest
    # username_loc = db.Column(String(255), nullable=True)
    
    # TODO: uncommment with first token quest
    # token_loc = db.Column(String(255), nullable=True)
    
    # authentication
    auth_type = db.Column(String(255), nullable=False)
    
    #execution settings
    is_stateless = db.Column(db.Boolean, default=False)
    solution_expected = db.Column(Text, nullable=True)
    solution_key = db.Column(String(255), nullable=True)
    solution_location = db.Column(String(255), nullable=True)
    execution_req_method = db.Column(String(255), nullable=False)
    execution_strategy = db.Column(String(255), nullable=False)
    
    #relationships
    prev_quest_id = db.Column(
        db.Integer,
        db.ForeignKey("quest.id"),
        nullable=True)

    prev_quests = db.relationship(
        "Quest",
        remote_side=[id],
        backref="next_quests")
    
    def __init__(self, title, **kwargs):
        self.title = title
        self.slug = slugify(title)
        #print("KWARGS IN INIT:", kwargs)
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
        quest = cls.query.filter_by(slug=slug).first()
        # if not quest:
        #     raise ValueError(f'Could not find Quest from slug: {slug}.')
        return quest

    def __repr__(self):
        return (f'<Quest id={self.id}, '
                f'title="{self.title}>')
    
    @validates('auth_type')
    def validate_auth_type(self, key, value):
        assert value in get_enum_values_as_list(AuthType)
        return value
    
    @validates('execution_strategy')
    def validate_execution_strategy(self, key, value):
        assert value in get_enum_values_as_list(QuestExecutionStrategy)
        return value
    
    @validates('username_loc', 'token_loc', 'answer_loc')
    def validate_input_location(self, key, value):
        #check against the saveable quest states
        valid_values = [e.value for e in InputLocation]
        if value not in valid_values:
            raise ValueError(
                (f'Invalided input locatoin value ({value}).'
                 f' allowed: {valid_values}')
            )
        return value
    
    # VALIDATE ALLOWED_METHODS
    @validates('allowed_req_methods')
    def validate_get_is_always_allowed(self, key, value: str):
        # GET must always be included
        methods = get_clean_list_from_string(value, ",")
        assert 'GET' in methods
        
        # validate methods are supported
        methods = get_clean_list_from_string(value, ",")
        valid_values = ['GET', 'POST', 'PUT', 'DELETE']
        assert set(methods).issubset(set(valid_values))
    
        return value
    
    @validates('form_keys')
    def validate_form_keys_are_allowed(self, key, value):
        if value:
            valid = get_enum_values_as_list(QuestKey)
            assert value in valid
        return value
    
    def validate(self):
        self.validate_solution_settings()
    
    def validate_req_method_settings(self):
        # when quest has an execution_req_method, then it must also be in allowed_req_methods
        if self.execution_req_method:
            allowed_methods = utils.get_clean_list_from_string(
                self.allowed_req_methods, ",")
            assert self.execution_req_method in allowed_methods
            
    def validate_solution_settings(self):
        if self.solution_expected:
            assert self.solution_location is not None
            assert self.solution_key is not None
            
        if self.solution_location:
            assert self.solution_expected is not None
            assert self.solution_key is not None
            
        if self.solution_key:
            assert self.solution_expected is not None
            assert self.solution_location is not None
