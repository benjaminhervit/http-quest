from typing import Any
from app.models import User


def get_progress_matrix() -> tuple[list[str], dict[str, Any]]:
    # rows = get_all_users_states()
    # quests = sorted({r["quest"] for r in rows})
    # users = sorted({r["username"] for r in rows})
    # table = []
    # for u in users:
    #     row = {"username": u}
    #     for q in quests:
    #         row[q] = next(
    #             (r["state"] for r in rows if r["username"] == u and r["quest"] == q), ""
    #         )
    #     table.append(row)
    return [], {}


# def get_all_users_states() -> list[dict[str, Any]]:
#     return [s.to_dict() for s in UserQuestState.query.all()]


def get_all_users_dicts() -> list[dict[str, Any]]:
    return [user.to_dict() for user in User.get_all()]
