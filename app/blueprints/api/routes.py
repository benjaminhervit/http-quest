from flask import jsonify

from app.blueprints.api import bp
from app.models.user import User
from app.enums import StatusCode

@bp.route('/all_users', methods=['GET'])
def get_all_users():
    dict_users = [user.to_dict() for user in User.get_all()]
    return jsonify(dict_users), StatusCode.OK.value
