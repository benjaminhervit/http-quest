from app.blueprints.quests import bp


# from app.request_manager import RequestManager


@bp.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
def welcome(path):
    return "This is just a game. Extend welcome on your path and you can begin."