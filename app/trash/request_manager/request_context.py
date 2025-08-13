from dataclasses import dataclass

from app.models import Quest, User

@dataclass
class RequestContext:
    user: User | None
    parsed: dict
    quest: Quest
    state: str