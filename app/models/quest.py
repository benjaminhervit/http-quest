from sqlalchemy import Integer, String, Text
from slugify import slugify
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import Base
from app.enums import InputLocation, ReqMethodType

class Quest(db.Model, Base):
    __tablename__ = "quest"
    
    # route and identifier
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    slug = db.Column(String(255), nullable=False, index=True)
    
    # content
    title = db.Column(String(255), nullable=False, index=True)
    directions = db.Column(Text, nullable=False)
    story = db.Column(Text, nullable=False)
    success_response = db.Column(Text, nullable=False)
    failed_response = db.Column(Text, nullable=False)
    is_locked_response = db.Column(Text, nullable=False)
    is_completed_response = db.Column(Text, nullable=False)
    
    # request settings
    allowed_req_methods = db.Column(String(255), nullable=True)
    
    expects_query = db.Column(db.Boolean, nullable=False)
    query_keys = db.Column(String(255), nullable=True)
    
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
    quest_description = db.Column(Text, nullable=True)
    expected_solution = db.Column(Text, nullable=True)
    execution_req_method = db.Column(String(255), nullable=False)
    execution_strategy = db.Column(String(255), nullable=False)
    answer_key = db.Column(String(255), nullable=True)
    answer_loc = db.Column(String(255), nullable=True)
    
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