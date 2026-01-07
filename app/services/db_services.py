from typing import Any
from app.models import User


def get_progress_matrix() -> tuple[list[str], dict[str, Any]]:
    return [], {}


def get_all_users_dicts() -> list[dict[str, Any]]:
    return [user.to_dict() for user in User.get_all()]


def get_user_quest_states(username: str) -> list[str]:
    user = User.get_by_username(username)
    print(type(user))
    if not user:
        return []
    quest_states = [user.start_quest, user.register_quest, user.identify_quest, user.jason_quest]
    return quest_states


def get_leaderboard() -> list[dict[str, any]]:
    users = User.get_all()
    leaderboard = []
    for user in users:
        leaderboard.append({
            "username": user.username,
            "xp": user.xp,
            "quest_states": get_user_quest_states(user.username)
        })
    return leaderboard