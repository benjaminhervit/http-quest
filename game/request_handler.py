from flask import Flask, request

from game.status_code import StatusCode
from game.level import Level, LevelEnum

def create_default_response(level:Level):
    failed_request_level_response = level.get_failed_request_info()
    response = {'request_status':StatusCode.BAD_REQUEST.value,
                'level_info': failed_request_level_response}
    return response

def validate_request(_request, target_method, username, username_registered):
    #validates method and user
    #default report
    request_report = {'request_accepted':False} #assume failure

    #method validation
    m_report = create_method_report(_request, target_method)
    request_report.update({'method_validation':m_report})

    #user validation
    u_report = create_user_validation_report(username, username_registered)
    request_report.update({'user_validation':u_report})

    if m_report['accepted'] and u_report['accepted']:
        request_report.update({'request_accepted':True})
    
    return request_report

def create_level_response(req_params, level:Level, next_level:Level, level_response_func:callable):
    answer = req_params.get('answers','')
    username = req_params.get('username','')
    level_info = level_response_func(level = level, next_level=next_level, answer= answer, username=username)
    return level_info

def rebuild_route(level, party_name=None, *answers):
    route = level
    if party_name:
        route = route + "/<string:username>"
        if answers:
            for a in range(0, len(answers)):
                route = route + f"/<string:answer{a}>"
    return route

def get_params_from_path(request)->dict:
    #should at least get level, and username - answers if level applicable
    path_params = dict()
    for key, value in request.view_args.items():
        path_params.update({key:value})

    #build answer
    answer_concat = ""
    answer_concat += request.args.get('answerA','').strip().lower()
    answer_concat += request.args.get('answerB','').strip().lower()
    answer_concat += request.args.get('answerC','').strip().lower()
    answer_concat += request.args.get('answerD','').strip().lower()
    if answer_concat:
        path_params.update({'answer': answer_concat})
    return path_params

def get_params_from_form_body(_request)->dict:
    form_params = {key: value for key, value in _request.form.items()}
    return form_params

def get_params_from_json_body(_request)->dict:
    try:
        json_params = _request.get_json()
        print(json_params)
        if json_params is None:
            json_params = {}
    except Exception as e:
        json_params = {}
    return json_params

def create_method_report(_request, target_method):
    report = {'method':_request.method,
              'target_method':target_method,
              'accepted':_request.method == target_method
              }
    return report

def create_user_validation_report(username, is_registered):
    user_report ={
        'username':username,
        'found_in_request':True if username else False,
        'is_registered': is_registered
        }
    user_report['accepted'] = True if is_registered and user_report['found_in_request'] else False
    return user_report

def create_level_welcome_response(**kwargs):
    level:Level = kwargs.get('level',None)
    return level.get_welcome_info() if level else "create_level_welcome_response() did not receive a level"

def create_level_answer_response(**kwargs):
    level:Level = kwargs.get('level',None)
    next_level:Level = kwargs.get('next_level',None)
    answer:str = kwargs.get('answer','')
    username:str = kwargs.get('username','')

    answer_success = level.answer_is_correct(answer)
    game_body = level.get_victory_info(username, next_level) if answer_success else level.get_wrong_answer_info()
    game_body.update({'next_level':next_level.directions if answer_success else "One level at a time..."})
    game_body.update({'answer_accepted':answer_success})

    return game_body