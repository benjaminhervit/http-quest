from dataclasses import dataclass, field
from slugify import slugify

from .base import Serializable


@dataclass
class QuestData(Serializable):
    title: str
    start_message: str
    quest: str
    completed: str
    locked: str
    next_path: str
    url_prefix: str
    xp: int
    learning: str
    hints: list[str] = field(default_factory=list)
    failed: str = field(default="Ah that is wrong! Try again {HERO}")
    path: str = field(init=False)
    slug: str = field(init=False)

    def __post_init__(self):
        self.slug = slugify(self.title)
        self.path = self.url_prefix + "/" + self.slug
