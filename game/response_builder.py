"""
Response builder validates different parts of the requests 

Returns:
    _type_: _description_
"""

from game.level import Level
from game.status_code import StatusCode
from quest_db import QuestDB

def create_data_response(token_found, token, is_registered):
    response = {'success':False, 'status_code':StatusCode.BAD_REQUEST.value,
                'token_found':token_found, 'is_registered':is_registered, 'party':token, 
                'message':'Two options: You are spellingly challenged, have not registered yet, or still struggling with how/where to put the data... okay.. three options maybe'
                }
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
    
def create_answer_response(level:Level, next_level:Level, answer, party, party_status, method_status):
    answer_status = level.answer_is_correct(answer)
    
    response = {'success':False, 'answer_status':answer_status,
                'party_status': party_status, 'method_status' : method_status, 
                'status_code':StatusCode.ACCEPTED.value, 'user_answer': answer, 
                'message' : f'You got close but your answer is not correct. Take a look at your . Quest: {level.riddle} Hint: {level.hint}'}
    
    #update if answer is correct
    if answer_status and party_status and method_status:
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