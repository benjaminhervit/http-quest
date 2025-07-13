from dataclasses import dataclass, field, asdict
from typing import Dict, Any
from enum import Enum
import json

from app.request_handler.enums import RequestEnums as RE

@dataclass
class Quest:
    """
    A data class making it more type safe to create level settings with enums and convert to json
    """
    title: str
    directions: str = field(init=False)
    
    welcome_text: str
    description: str
    quest: str
    answer: str

    response_wrong: str
    response_correct: str
    response_completed: str

    next_quest_directions: str

    request_settings: Dict[RE, Dict[RE, RE]]

    def __post_init__(self):
        self.directions = f"GET here by going to game/quest/{self.title}"
        
    def to_dict(self):
        def convert(obj):
            if isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, dict):
                return {convert(k): convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            return obj

        return convert(asdict(self))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)