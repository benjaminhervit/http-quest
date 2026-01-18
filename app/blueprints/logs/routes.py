from flask import render_template

from . import bp
from app.models import LastUserRequestLog


@bp.route("/last_request" + "/<username>", methods=["GET"])
@bp.route("/last_request", methods=["GET"])
def last_request(username=None):
    if username:
        last_req = LastUserRequestLog.get_users_last_request(username)
        return render_template("logging.html", log=last_req)
    return render_template("logging.html")