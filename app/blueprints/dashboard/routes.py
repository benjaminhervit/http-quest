from flask import jsonify, request

from app.blueprints.dashboard import bp

from app.models.user import User
from app.enums import StatusCode


@bp.route("/")
def data_dump():
    users = [u.to_dict() for u in User.query.all()]
    return jsonify({"users": users})


# @bp.route("/all-user-quest-states", methods=["GET"])
# def all_quest_states():
#     data = [q.to_dict() for q in UserQuestState.query.all()]
#     if not data:
#         return jsonify({"error": "No data found"}), StatusCode.SERVER_ERROR.value

#     return jsonify({"data": data}), StatusCode.OK.value


# @bp.route("/all-quests", methods=["GET"])
# def all_quests():
#     quests = [q.to_dict() for q in Quest.query.all()]
#     if not quests:
#         return jsonify({"error": "No quests found"}), StatusCode.SERVER_ERROR.value

#     return jsonify({"quests": quests}), StatusCode.OK.value


@bp.route("/user")
def user_data():
    query: dict = request.args.to_dict()
    print(query)
    if query is None:
        return "Did not receive any query params."
    username = query.get("username")
    if username is None:
        return "Found no username in query."

    user_obj = User.query.filter_by(username=username).first()
    if user_obj is None:
        return f"Username {username} is not registered."

    return (
        jsonify(
            {
                "username": username,
                "data": user_obj,
            }
        ),
        StatusCode.OK,
    )
