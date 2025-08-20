from .auth.data import get_quest as auth_quest
from .start.data import get_start_quest as start_quest
from .identify_yourself.data import get_quest as identify_quest
from .jason_quest.data import get_quest as jason_quest


def get_all_quests():
    return [auth_quest(), start_quest(), identify_quest(), jason_quest()]

def get_quest_by_title(title: str):
    auth_q = auth_quest()
    
