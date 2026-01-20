from typing import Any
from app.models import User
from app.enums import QuestTitle


def get_progress_matrix() -> tuple[list[str], dict[str, Any]]:
    return [], {}


def get_all_users_dicts() -> list[dict[str, Any]]:
    return [user.to_dict() for user in User.get_all()]


def get_user_quest_states(username: str) -> list[str]:
    user = User.get_by_username(username)
    if not user:
        return []
    quest_states = [user.start_quest, 
                    user.register_quest, 
                    user.identify_quest,
                    user.jason_quest, 
                    user.wall_quest, 
                    user.git_monster_quest,
                    user.beg_quest, 
                    #user.the_crown_quest
                    ]
    return quest_states


def get_user_quest_values(username: str) -> list[str]:
    user = User.get_by_username(username)
    if not user:
        return []
    quest_states = [qs_to_lb(user.start_quest), 
                    qs_to_lb(user.register_quest), 
                    qs_to_lb(user.identify_quest),
                    qs_to_lb(user.jason_quest), 
                    qs_to_lb(user.wall_quest), 
                    qs_to_lb(user.git_monster_quest),
                    convert_beg_quest_to_leaderboard(username, user.beg_quest), 
                    #qs_to_lb(user.the_crown_quest)
                    ]
    return quest_states


def qs_to_lb(quest_state: str) -> str:
    if quest_state == "locked":
        return "x"
    if quest_state == "unlocked":
        return "0"
    if quest_state == "completed":
        return "1"

    
def convert_beg_quest_to_leaderboard(username, quest_state: str) -> str:
    if quest_state == "locked":
        return "x"
    return str(User.get_beg_counter(username))


def get_leaderboard() -> list[dict[str, any]]:
    users = User.get_all()
    leaderboard = []
    for user in users:
        leaderboard.append({
            "username": user.username,
            "xp": user.xp,
            "quest_states": get_user_quest_states(user.username),
            "quest_values": get_user_quest_values(user.username)
        })
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)
    return leaderboard