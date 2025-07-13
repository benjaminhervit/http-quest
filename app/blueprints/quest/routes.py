from flask import request, jsonify
import json

from app.blueprints.quest import bp

from app.request_handler.handler import RequestHandler
from app.request_handler.enums import RequestEnums as RE
from app.errors import MissingData

from app.game.quests import quests

# class Quest:
#     def __init__(self):
#         #REQUEST PARAMS
#         self.request_settings = {
#             'GET':{
#                 RE.BODY_TYPE : RE.PATH,
#                 RE.AUTH_TYPE : RE.AUTH_BY_USERNAME,
#                 RE.USERNAME_LOCATION : RE.PATH,
#                 }
#         }
        
#         self.POST_SETTINGS = {}

#         #QUEST SPECIFIC
#         self.title = "Welcome"
#         self.directions = f"GET here by going to game/quest/{self.title}"

#         #
#         self.welcome_text = "Welcome to a CRUDe game!"
#         self.description = "You stand in front of an epic quest with nothing but your hard earned knowledge from a lecture you never attended."
#         self.quest = "Write your name in the PATH to glory"
#         self.answer = "TestAnswer"

#         #responses
#         self.response_wrong = "Absolutely not correct - not even one bit. I mean... holy..!"
#         self.response_correct = "What a genius you are! This is out standing! The world will soon be safe again!"
#         self.response_completed = "why are you still here???"

#         #next level/quest
#         self.next_quest_directions = "there should be some/path/descriptions/here"

#     def __repr__(self):
#         return f'<Post "{self.title}">'

# q1 = Quest()
# quests = {q1.title.strip().lower() : q1}

@bp.route('<quest_id>', defaults={'path':''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('<quest_id>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def quest(quest_id, path):
    try:
        #get quest
        quest_obj:Quest = quests.get(quest_id)
        if not quest_obj:
            raise MissingData('That quest does not exist here. Maybe double check it?')
        
        #validate request format
        rh = RequestHandler(quest_obj.request_settings, request, path)
        response, status = rh.validate()
        if status is not RE.STATUS_OK.value:
            return response, status
        
        #run game
        session = PlayerQuestSession.query.filter_by(username=username).first()
        if not session:
            raise MissingData(f'Session for player {response.get('username')} and quest {quest_obj.title} not found. This is a server side problem.')
        
        
        return jsonify({'message':'FUCK YES'}), RE.STATUS_OK.value
    except MissingData as e:
        return jsonify({'error': str(e)}), RE.STATUS_BAD_REQUEST.value