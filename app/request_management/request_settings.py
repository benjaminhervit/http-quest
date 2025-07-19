from dataclasses import dataclass, asdict
import json

@dataclass
class RequestSettings:
    req_method:str
    username_location:str
    
    answer_location:str
    answer_key:str
    
    auth_type:str
    token_location:str
    
    def to_dict(self):
        """
        Make sure all enums gets converted to str or int values
        """
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)