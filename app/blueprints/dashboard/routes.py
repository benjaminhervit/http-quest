from flask import jsonify, request

from app.blueprints.dashboard import bp

from app.extensions import db
from app.models.quest import Quest
from app.models.user import User
from app.models.user_quest_state import UserQuestState
from app.enums import StatusCode

@bp.route('/')
def data_dump():
    states = [s.to_dict() for s in UserQuestState.query.all()]
    users = [u.to_dict() for u in User.query.all()]
    quests = [q.to_dict() for q in Quest.query.all()]
    return jsonify(
                   {
                       'users': users,
                       'questes': quests,
                       'states': states
                   })
    
@bp.route('/user')
def user_data():
    query: dict = request.args.to_dict()
    print(query)
    if query is None:
        return "Did not receive any query params."
    username = query.get('username')
    if username is None:
        return "Found no username in query."
    
    user_obj = User.query.filter_by(username=username).first()
    if user_obj is None:
        return f"Username {username} is not registered."
    
    quest_states: list[UserQuestState] | None = (
        UserQuestState.query.filter_by(
            username=username
            ).all())
    if quest_states is None:
        return f"Could not find any quests states for {username}. Talk to a dev please."
    
    return jsonify(
        {
          'username': username,
          'quest_states': [qs.to_dict() for qs in quest_states]
        }
    ), StatusCode.OK