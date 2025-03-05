"""
Response builder validates different parts of the requests 

Returns:
    _type_: _description_
"""

from game.level import Level
from game.status_code import StatusCode
from quest_db import QuestDB
import random

def build_request_report(method, target_method, method_success, party_name_found, party_name, party_is_registered, party_success, request_success):
    report = {
            'success':request_success,
            'method': method, 'target_method':target_method, 'method_success':method_success,
            'party_name':party_name, 'party_name_found':party_name_found,
            'party_is_registered':party_is_registered, 'party_success':party_success
        }
    
    #method check and logs
    # report.update({'method':method})
    # report.update({'target_method':method})
    # method_success = method == target_method
    # report.update({'method_success':method_success})
    
    #party name check and logs
    # report.update({'party_name_found':party_name_found})
    # report.update({'party_name':party_name})    
    
    # report.update({'party_is_registered':party_is_registered})
    
    # party_success = party_name_found and party_is_registered
    # report.update({'party_success':party_success})
    return report


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

def create_standard_response_body(level:Level):
    return {'success' : False, 'party_found':False, 'party':"", 'is_registered': False, 'party_success':False,
            'message' :  "Standard response body - you should not receive this. Talk to a TA.",
            'status_code' : StatusCode.BAD_REQUEST.value,
            'level_info': level.directions, #will only include directions to the level until they pass method and party test
            'method_found':"", 'method_target':"", 'method_success':False,
            'answer_status':False, 'answer_from_user':""
            }

def add_method_validation_to_response(method, target_method, response:dict):
    #dummy message to find loop holes
    response.update({'message':'Method validation update - if you see this you should tell a TA.'})
    
    #update fields
    response.update({'method_used' : method })
    response.update({'method_target' : target_method})
    
    #update with validation
    # #is themethod used the same as the method that was intended?
    method_accepted = method == target_method
    response.update({'method_success' : method_accepted})
    response.update({'message' : response['message'] if method_accepted else 'You need to work on the METHODology.'})
    response.update({'status_code':StatusCode.ACCEPTED.value if method_accepted else response['status_code']})

def update_response_with_party_validation( party_found, party, is_registered, response:dict):
    #dummy message to find loop holes
    response.update({'message':'Party validation update - if you see this you should tell a TA.'})
    
    #update fields
    response.update({'party_found':party_found})
    response.update({'party':party})
    response.update({'is_registered' : is_registered})
    
    #update with party validation: 
    # #did we found the party field in the request? 
    # #did we found a valid value in the party field? 
    # #is the party registered in the db?
    party_accepted = party_found and party and is_registered
    response.update({'party_success':party_accepted})
    response.update({'message':'This party is fine.' if party_accepted else 'Either you miss spelled your party or it is already registered by someone else?'})
    
def update_response_with_answer_validation(level:Level, next_level:Level, answer, response:dict):
    """
    Assumes that the response has already gone through method and party validation.

    Returns:
        _type_: _description_
    """
    #dummy message to find loop holes
    response.update({'message':'Answer validation update - if you see this you should tell a TA.'})
    
    #update fields
    response.update({'answer_status':False})
    response.update({'answer_from_party': answer})
    response.update({'level_info':level.get_wrong_answer_info}) #assume failure
    
    #update with validation
    answer_status = level.answer_is_correct(answer)
    quest_completed = answer_status and response['method_status'] and response['party_status']
    
    #update if answer is correct
    if quest_completed:
        response.update({'success':True})
        level_info = level.get_victory_info(response['party'])
        level_info.update({'directions_to_next_level': next_level.directions})
        response.update({'level_info':level_info})
        response.update({'message':random.choice(victory_lines)})
        response.update({'status_code': StatusCode.OK.value})
    return response

def create_level_welcome_response_body(level:Level):
    return {'success':True, 'level_info' : level.get_welcome_info, 'status_code':StatusCode.OK.value}

