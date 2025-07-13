from flask import request, jsonify
import json

from app.blueprints.quest import bp

from app.request_handler.handler import RequestHandler
from app.request_handler.enums import RequestEnums as RE
from app.errors import MissingData

from app.game.quests import quests
from app.game.quests.quest import Quest
from app.game.quests.session import QuestSession

@bp.route('<quest_id>', defaults={'path':''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('<quest_id>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def quest(quest_id, path):
    try:
        #get quest
        quest_obj: Quest= quests.get(quest_id)
        if not quest_obj:
            raise MissingData('That quest does not exist here. Maybe double check it?')
        
        #validate request format
        rh = RequestHandler(quest_obj.request_settings, request, path)
        response, status = rh.validate()
        if status is not RE.STATUS_OK.value:
            return response, status
        
        #run game
        session = QuestSession(quest_obj, rh)
        
        return session.run()
        #session = PlayerQuestSession.query.filter_by(username=username).first()
        #if not session:
        #    raise MissingData(f'Session for player {response.get('username')} and quest {quest_obj.title} not found. This is a server side problem.')
        
        
        return jsonify({'message':'FUCK YES'}), RE.STATUS_OK.value
    except MissingData as e:
        return jsonify({'error': str(e)}), RE.STATUS_BAD_REQUEST.value