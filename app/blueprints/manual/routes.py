from flask import render_template

from app.blueprints.quests import bp

@bp.route("/manual", methods=["GET"])
def manual():
    return render_template('manual.html')
