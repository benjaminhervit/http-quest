
from flask import jsonify

from level import Level
from status_code import StatusCode
from quest_db import QuestDB

def handle_request(target_method, level:Level, next_level:Level,
                    get_secret_key:callable, get_data:callable, 
                    level_response:callable, db:QuestDB, req):
    #set default response
    failed_request_level_response = level.get_failed_request_info()
    response = {'request_status':StatusCode.BAD_REQUEST.value,
            'level_info': failed_request_level_response}
    
    #build request report
    if not req.method == target_method:
        response.update({'request_status': StatusCode.UNAUTHORIZED.value, 'error': 'You must work on the METHODology.'})
        return jsonify(response), 404 #big failure
    response.update({'method_status': 'accepted'})
    
    # Retrieve X-secret-key from request headers
    secret_key = get_secret_key(req)
    user_validated = secret_key and db.get_team(secret_key) is not None
    if not user_validated:
        response.update({'request_status': StatusCode.UNAUTHORIZED.value, 'error': 'Missing the secret key ingredient X'})
        return jsonify(response), 404 #big failure
    response.update({'secret-key': 'accepted'})
    response.update({'request_status':StatusCode.ACCEPTED.value}) #upgrades status to indicate method and username is handled correct

    request_data = get_data(req)
    
    #build level response
    answer = request_data.get('answers','')
    print("HERE!")
    level_info = level_response(level=level, answer=answer, next_level=next_level, username=secret_key)
    print(f"FROM LEVEL: {level_info}")
    response.update({'level_info':level_info})
    
    #check if level completed
    answer_accepted = level_info.get('answer_accepted','')
    if answer_accepted:
        response.update({'request_accepted':True})
        response.update({'request_status':StatusCode.OK.value})
    
    return jsonify(response)

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

def none_method(*args):
    return None

def get_params_from_form_body(_request)->dict:
    form_params = {key: value for key, value in _request.form.items()}
    return form_params

def get_secret_key_from_path(req):
    return req.view_args.get('username', '')

def get_secret_key_from_header(req):
    return req.headers.get('X-secret-key', '')

def get_params_from_json_body(req)->dict:
    return req.get_json()