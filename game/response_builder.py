"""
Response builder validates different parts of the requests 

Returns:
    _type_: _description_
"""

from game.level import Level
from game.status_code import StatusCode
from quest_db import QuestDB
import random

victory_lines = [
            "HTTP 200: OK! You've conquered this level!",
            "Request successful! You've leveled up!",
            "Status 200: Victory achieved!",
            "You've sent the right request and got the best response!",
            "Your answer was a GET request for glory, and you got it!",
            "POSTing this victory to your achievements!",
            "You've PUT in the effort and it paid off!",
            "PATCHing your status to victorious!",
            "DELETE all doubts, you did it!",
            "OPTIONS: Celebrate or Celebrate? Choose wisely!"
        ]

def create_next_level_dict(level:Level, next_level:Level, party):
    #combining next level and current level info
    level_as_dict = {
        "current_level":level.name,
        "next_level":'You will now when you get there',
        "story":level.victory_message_template.format(party=party),
        "directions_to_next_level":next_level.directions,
        "to_stay_here":level.directions
    }
    return level_as_dict

def create_level_dict(level:Level):
    #doing it here to avoid oversharing
    level_as_dict = {
        "name":level.name,
        "story":level.description,
        "quest":level.quest,
        "hint":level.hint,
        "to_stay_here":level.directions,
        "directions_to_next_level":"First you must complete your quest."
    }
    return level_as_dict

def create_data_response(level:Level, token_found, token, is_registered):
    level_dict = create_level_dict(level)
    print(f"DATA LEVEL DICT TYPE: {type(level_dict)}")
    response = {'success':False, 'status_code':StatusCode.BAD_REQUEST.value,
                'token_found':token_found, 'is_registered':is_registered, 'party':token, 
                'message':'Two options: You are spellingly challenged, have not registered yet, or still struggling with how/where to put the data... okay.. three options maybe',
                'level_info': level_dict
                }
    if response['party'] and response['is_registered']:
        response.update({'success':True})
        response.update({'status_code': StatusCode.ACCEPTED.value})
        response.update({'message':'This party is fine'})
    return response

def create_method_response(level:Level, method, target_method):
    level_dict = create_level_dict(level)
    print(f"METHOD LEVEL DICT TYPE: {type(level_dict)}")
    return {'success' : method == target_method,
            'message' :  "" if method == target_method else 'You need to work on the METHODology.',
            'method_used' : method,
            'status_code' : StatusCode.ACCEPTED.value if method == target_method else StatusCode.BAD_REQUEST.value,
            'level_info': level_dict
            }
    
def create_answer_response(level:Level, next_level:Level, answer, party, party_status, method_status):
    answer_status = level.answer_is_correct(answer)
    level_dict = create_level_dict(level)
    print(f"ANSWER LEVEL DICT TYPE: {type(level_dict)}")
    response = {'success':False, 'answer_status':answer_status,
                'party_status': party_status, 'party':party, 
                'method_status' : method_status, 
                'status_code':StatusCode.ACCEPTED.value, 'user_answer': answer,
                'level_info': level_dict,
                'message' : 'You got close but your answer is not correct. Read through the level information and try again. There is only one path and answer buy many ways travel.'}
    
    #update if answer is correct
    if answer_status and party_status and method_status:
        response.update({'success':True})
        response.update({'error':'No errors here!'})
        level_dict = create_next_level_dict(level, next_level, party)
        print(f"SUCCES LEVEL DICT TYPE: {type(level_dict)}")
        response.update({'level_info':level_dict})

        response.update({'victory_line': random.choice(victory_lines)})
        response.update({'message':random.choice(victory_lines)})
        
        response.update({'status_code': StatusCode.OK.value})
    return response

def create_level_welcome_response(level:Level):
    msg = level.description
    msg += " " + level.quest + " " + level.hint
    return {'success':True, 'message' : msg, 'status_code':StatusCode.OK.value}