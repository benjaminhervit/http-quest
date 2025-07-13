from flask import request, jsonify

from app.blueprints.quest import bp
from app.request_handler.request_handler import RequestHandler
from app.request_handler.enums import RequestParams as RP

from app.errors import MissingData

class Quest:
    def __init__(self):
        #REQUEST PARAMS
        self.request_settings = {
            'GET':{
                RP.DATA_LOCATION : RP.PATH,
                RP.AUTH_TYPE : RP.AUTH_BY_USERNAME,
                RP.USERNAME_LOCATION : RP.PATH,
                RP.SECRET_KEY : None
                }
        }
        
        #QUEST SPECIFIC
        self.title = "Welcome"
        self.directions = "Get here by going to game/level/welcome"
        
        #
        self.welcome_text = "Welcome to a CRUDe game!"
        self.description = "You stand in front of an epic quest with nothing but your hard earned knowledge from a lecture you never attended."
        self.quest = "Write your name in the PATH to glory"
        self.answer = "TestAnswer"
        
        #responses
        self.response_wrong = "Absolutely not correct - not even one bit. I mean... holy..!"
        self.response_correct = "What a genius you are! This is out standing! The world will soon be safe again!"
        self.response_completed = "why are you still here???"
        
        #next level/quest
        self.next_quest_directions = "there should be some/path/descriptions/here"
    
    def __repr__(self):
        return f'<Post "{self.title}">'

q1 = Quest()
quests = {q1.title : q1}

@bp.route('<quest_id>', defaults={'path':''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('<quest_id>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def welcome(quest_id, path):
    try:
        quest = quests.get(quest_id)
        if not quest:
            raise MissingData('That quest does not exist here. Maybe double check it?')
            
        rh = RequestHandler(quest.request_settings, request)
        response, status = rh.validate()
        if status is not RP.STATUS_OK.value:
            return response, status
        
        #response, status GM.run_quest()
        
        return jsonify({'message':'FUCK YES'}), RP.STATUS_OK.value
    except MissingData as e:
        return jsonify({'error': str(e)}), RP.STATUS_BAD_REQUEST.value