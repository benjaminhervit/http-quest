from typing import Any
from app.models import User
from app.enums import QuestTitle


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

# def get_user_quest_states_as_list(username: str) -> list[str]:
#     user = User.get_by_username(username)
#     print(type(user))
#     if not user:
#         return []
#     print(f"User attributes: {vars(user)}")
#     print(f"User dict: {user.__dict__}")
#     for attr in dir(user):
#         if not attr.startswith('_'):
#             print(f"{attr}: {getattr(user, attr, None)}")
#     quest_states = [ 
#                     {QuestTitle.START_QUEST.value: user.start_quest},
#                     {QuestTitle.REGISTER_QUEST.value: user.register_quest},
#                     {QuestTitle.IDENTIFY_QUEST.value: user.identify_quest},
#                     {QuestTitle.JASON_QUEST.value: user.jason_quest},
#                     ]
#     return quest_states
    