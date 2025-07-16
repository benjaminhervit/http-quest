from dataclasses import dataclass, field, asdict
from typing import Dict
from enum import Enum
import json

@dataclass
class Quest:
    """
    A data class making it more type safe to create level settings with enums and convert to json
    """
    title: str
    route: str = field(init=False)
    directions: str
    
    welcome_text: str
    description: str
    quest: str
    correct_answer: str

    response_wrong: str
    response_correct: str
    response_completed: str

    next_quest_directions: str

    request_settings: Dict[str, Dict[str, str]]
    answer_settings: Dict[str, Dict[str, str]]

    def __post_init__(self):
        self.route = self.title.strip().lower().replace(' ', '_')

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
            return obj

        return convert(asdict(self))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)