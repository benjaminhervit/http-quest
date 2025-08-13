from dataclasses import dataclass, asdict, field
import json
from slugify import slugify

from app.models import Quest
from app.extensions import db

@dataclass
class Serializable:
    def to_dict(self):
        return asdict(self)
    
    def to_json(self, json_kwargs):
        return json.dumps(self.to_dict(), **json_kwargs)
    
@dataclass
class QuestData(Serializable):
    title: str
    start_message: str
    quest: str
    completed: str
    locked: str
    next_path: str
    hint: str
    url_prefix: str
    path: str = field(init=False)
    slug: str = field(init=False)
    
    def __post_init__(self):
        self.slug = slugify(self.title)
        self.path = self.url_prefix + "/" + self.slug
        
        
        print(f"Saving {self.title} to database")
        if not Quest.quest_exists(self.title):
            quest: Quest = Quest(title=self.title,
                                 path=self.path)
            db.session.add(quest)
            db.session.commit()