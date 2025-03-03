"""Response builder validates different parts of the requests 

Returns:
    _type_: _description_
"""

from level import Level
from status_code import StatusCode
from quest_db import QuestDB

def create_data_response(token_found, token, db:QuestDB):
    response = {'success':False,'token':False, 'is_registered':False, 'party':None, 'status_code':StatusCode.BAD_REQUEST.value}
    response.update({'token': token_found})
    if response['token']:
        response.update({'party':token})
        response.update({'is_registered': db.get_team(token) is not None})
    else:
        response.update({'message':'Two options: You are spellingly challenged or you have not registered yet.'})
    if response['token'] and response['is_registered']:
        response.update({'success':True})
        response.update({'status_code': StatusCode.ACCEPTED.value})
        response.update({'message':'This party is fine'})
    return response

def create_method_response(method, target_method):
    return {'success' : method == target_method,
            'message' :  "" if method == target_method else 'You need to work on the METHODology.',
            'method_used' : method,
            'status_code' : StatusCode.ACCEPTED.value if method == target_method else StatusCode.BAD_REQUEST.value
            }
    
def create_answer_response(level:Level, next_level:Level, answer, party):
    response = {'success':False, 'user_answer':answer, 'message' : f'You got close but your answer is not correct. Quest: {level.riddle} Hint: {level.hint}', 'status_code':StatusCode.ACCEPTED.value}
    
    #update if answer is correct
    if level.answer_is_correct(answer):
        response.update({'success':True})
        response.update({'error':'No errors here!'})
        
        msg = level.victory_message_template.format(party=party)
        msg += next_level.directions
        response.update({'message':msg})
        
        response.update({'status_code': StatusCode.OK.value})
    return response

def create_level_welcome_response(level:Level):
    msg = level.description
    msg += " " + level.riddle + " " + level.hint
    return {'success':True, 'message' : msg, 'status_code':StatusCode.OK.value}