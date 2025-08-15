from dataclasses import dataclass, asdict
import json

@dataclass
class Serializable:
    def to_dict(self):
        return asdict(self)

    def to_json(self, json_kwargs):
        return json.dumps(self.to_dict(), **json_kwargs)