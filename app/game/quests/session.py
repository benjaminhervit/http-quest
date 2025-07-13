from flask import jsonify

from app.game.quests.quest import Quest
from app.game.enum import GameEnum as GE
from app.request_handler.enums import RequestEnums as RE
from app.errors import Unauthorized
from app.request_handler.handler import RequestHandler

class QuestSession:
    def __init__(self, quest_obj:Quest, req:RequestHandler):
        self.req:RequestHandler = req
        self.quest_obj = quest_obj
        self.status = GE.UNLOCKED
    
    def run(self):
        try:
            if self.status == GE.LOCKED:
                raise Unauthorized(f'User {self.username} has not unlocked {self.quest_obj.title} yet.')
            
            if self.status == GE.COMPLETED:
                return jsonify({'status':GE.COMPLETED, 'message':self.quest_obj.response_completed}), RE.STATUS_OK.value
            
            return jsonify(self.get_quest_response()), RE.STATUS_OK.value
    
        except Unauthorized as e:
            return jsonify({'error':str(e)}), RE.STATUS_UNAUTHORIZED
        
    def get_quest_response(self):
        quest_json:dict = self.quest_obj.to_dict()
        sub_keys = ['title', 'description', 'quest']
        return {key : quest_json.get(key) for key in sub_keys if key in quest_json}
    
    def get_answer_response(self):
        return "something...."