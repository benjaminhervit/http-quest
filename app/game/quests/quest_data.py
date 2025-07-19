from dataclasses import dataclass, field, asdict
from typing import Dict
from enum import Enum
import json
from app.request_management.request_settings import RequestSettings

@dataclass
class QuestData:
    """
    A data class making it more type safe to create level settings with enums and convert to json
    """
    #ROUTE
    
    #TXT
    q_id:str = field(init=False)
    title: str
    directions_txt: str
    story_txt: str
    quest_txt: str
    response_wrong_txt: str
    response_correct_txt: str
    response_completed_txt: str
    
    #LOGIC SETTINGS
    correct_answer: str
    quest_validator_type:str

    next_quest_directions: str
    
    #REQUEST SETTINGS
    route: str = field(init=False)
    request_settings : RequestSettings
    
    
    def __post_init__(self):
        self.route = self.title.strip().lower().replace(' ', '_')
        self.q_id = f"{self.route}_{self.request_settings.req_method}"

    def to_dict(self):
        """
        Make sure all enums gets converted to str or int values
        """
        def convert(obj):
            if isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, dict):
                return {convert(k): convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            elif isinstance(obj, RequestSettings):
                return {convert(k): convert(v) for k, v in obj.to_dict()}
            return obj

        return convert(asdict(self))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)