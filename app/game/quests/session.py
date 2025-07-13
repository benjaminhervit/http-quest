from flask import jsonify

from app.game.quests.quest import Quest
from app.game.enum import GameEnum as GE
from app.request_handler.enums import RequestEnums as RE
from app.errors import Unauthorized, SettingNotFound
from app.request_handler.handler import RequestHandler

class QuestSession:
    def __init__(self, quest_obj:Quest, req:RequestHandler):
        self.req:RequestHandler = req
        self.quest_obj = quest_obj
        self.status = GE.UNLOCKED
        
        self.response_actions = {
            RE.REQUEST_IS_GET_QUEST : self.get_quest_response,
            RE.REQUEST_IS_ANSWER : self.get_answer_response
        }
    
    def run(self):
        try:
            if self.status == GE.LOCKED:
                raise Unauthorized(f'User {self.username} has not unlocked {self.quest_obj.title} yet.')
            
            if self.status == GE.COMPLETED:
                return jsonify({'status':GE.COMPLETED, 'message':self.quest_obj.response_completed}), RE.STATUS_OK.value
            
            return jsonify(self.create_response()), RE.STATUS_OK.value
    
        except Unauthorized as e:
            return jsonify({'error':str(e)}), RE.STATUS_UNAUTHORIZED.value
        
        except SettingNotFound as e:
            return jsonify({'error':str(e)}), RE.STATUS_BAD_REQUEST.value
        
    def get_quest_response(self):
        quest_json:dict = self.quest_obj.to_dict()
        sub_keys = ['title', 'description', 'quest']
        return {key : quest_json.get(key) for key in sub_keys if key in quest_json}
    
    def get_answer_response(self):
        return {'message':'FUCK I MADE IT TO THE ANSWER POST!'}
    
    def create_response(self):
        response_type:RE = self.req.get_response_type()
        if not response_type:
            raise SettingNotFound('Could not find response type. This is a server side issue.')
        resp_body = self.response_actions.get(response_type)()
        if not resp_body:
            raise SettingNotFound(f'Could not generate response for {response_type.value}')
        return resp_body
        