"""
This is a HTTP/CRUD learning game, using Flask, SQLite and vanilla JS, HTML and Pico CSS.
In the game, a party must go through a set of riddles/challenges
to finally claim the CRUD crown and sit on the WoThrone™. 
There is a shared leader board for all registered players/parties, to see who is in the leader.

To play the game, the player must first register on through the index.html site. 
From here, they will have to use the information from ridles, hints, directions and descriptions to 
make the correct HTTP requests to go to the next level or answer a riddle/challenge.

The game should give the player handson experience with making various HTTP requests passing values through 
path params, forms, and JSON. All responses are returned as JSON.

The Player can choose however they want to defeat the game. Using python, JavaScript, Postman or anything else
doesn't really matter - as long as they create the correct requests to get familiar with the setup.

Returns:
    _type_: _description_
"""

from flask import Flask, render_template, redirect, url_for, request, g, abort, jsonify, Response, send_file, make_response
import mimetypes
import json
from urllib.parse import unquote, quote

from game.level import Level, LevelEnum as L
import game.level_builder as level_builder
from game.routes import Route as R
from game.status_code import StatusCode

import game.response_builder as RB

from quest_db import QuestDB
import random

app = Flask(__name__)

victory_messages = [
    "GET ready to move to the next level!",
    "PUT your skills to the test in the next challenge!",
    "DELETE all doubts, you've passed this level!",
    "You've PATCHed up this level's challenges!",
    "HEADs up, you're advancing!",
    "You've navigated through this level successfully!",
    "OPTIONS for the next level: ready or not, here you go!",
    "TRACE your steps, you've completed this level!",
    "CONNECT with the next challenge and keep going!"
]

def get_random_victory_message():
    return random.choice(victory_messages)

levels = {
    L.REGISTRATION: level_builder.createRegisterLevel(),
    L.THE_TEST: level_builder.createTheTestLevel(),
    L.THE_MONSTER : level_builder.createTheGitLevel(),
    L.THE_GATE : level_builder.createGateLevel(),
    L.THE_THRONE_ROOM : level_builder.createThroneLevel(),
    L.THE_CROWN : level_builder.createCrownLevel(),
    L.GAME_OVER : level_builder.createGameOverLevel()
}

all_methods = ['GET', 'POST', 'PUT', 'DELETE']

def build_request_report(method, target_method, party_name_found, party_name):
    #build request report
    method_success = method == target_method
    party_is_registered = False
    if party_name_found:
        party_in_db = get_game_db().get_team(party_name)
        party_is_registered = party_in_db is not None and len(party_in_db) > 0
    
    party_success = party_name_found and party_is_registered
    request_success = method_success and party_success
    request_report = {
            'success':request_success,
            'method': method, 'target_method':target_method, 'method_success':method_success,
            'party_name':party_name, 'party_name_found':party_name_found,
            'party_is_registered':party_is_registered, 'party_success':party_success
        }
    return request_report

def build_answer_response(level:Level, next_level:Level, answer, party):
    #build game body
    
    answer_success = level.answer_is_correct(answer)
    game_body = level.get_victory_info(party, next_level) if answer_success else level.get_wrong_answer_info()
    game_body.update({'next_level':next_level.directions if answer_success else "One level at a time..."})
    game_body.update({'success':answer_success})
    return game_body

def execute_level(level_name, default_level_response, target_method, method, 
                  party_name_found, party_name, level_answer_response):
    """
    Builds appropriate response based on the request and level requirements
    Returns:
        _type_: _description_
    """
    #standard response assumes failure
    report_request = build_request_report(method, target_method, party_name_found, party_name)
    response = {
            'request_report':report_request,
            'level_info':default_level_response,
            'level_completed':False,
            'status_code': StatusCode.BAD_REQUEST.value,
            'message': 'Seems like your answer or request was not on point. Go through the report and see if you can sport the issue? - maybe have a look at the level_info as well?'
            }
    if not report_request['success']:   
        return jsonify(response)
    
    response.update({'level_info':level_answer_response})
    level_completed = level_answer_response['success'] and report_request['success']
    if level_completed:
        response.update({'level_completed':True})
        response.update({'status_code':StatusCode.OK.value})
        response.update({'message': get_random_victory_message()})
        
        if get_game_db().update_level(party_name, level_name):
            get_game_db().update_score(party_name, 1)
        
    return jsonify(response)

#LEVEL 5: THE THRONE ROOM
@app.route(R.THE_CROWN.value, methods=all_methods)
def the_crown():
    party_name = ""
    party_name_found = False
    answer = ""
    feedback = ""
    
    if request.is_json:
            data = request.get_json()
            party_name = data.get('party_name', '').strip().lower()
            party_name_found = len(party_name)>0
            answer = data.get('answer', '').strip().lower()
            feedback = data.get('feedback', '').strip().lower()
    
    if len(feedback) > 0:
        print(f"FEEDBACK: {feedback}")
        #TODO STORE FEEDBACK SOMEWHERE
    
    level:Level = levels[L.THE_CROWN]
    next_level:Level = levels[L.GAME_OVER]
    level_response = build_answer_response(level, next_level, answer, party_name)
    response:Response = execute_level(level.name, level.get_failed_request_info(), 'PUT', request.method, party_name_found, party_name,level_response)
    
    response_data:dict = response.get_json()
    
    if response_data.get('level_completed'):
        level_info:dict = response_data['level_info']
        level_info.update({'description':f'Well played {party_name}. We hope you had fun and learned something along the way :)'})
        del response_data['level_info']['quest']
        del response_data['level_info']['next_level']
    send_png = request.headers.get('Victory-content', "").strip().lower()
    if send_png == "image/png":
        response.headers['From the TAs']='Thank you for playing.'
        png_path = "static/images/crown.png"
        return send_file(png_path, mimetype="image/png", as_attachment=True)
            
    response = jsonify(response_data)
    return response

@app.route(R.READ_JASONS_MIND.value, methods=all_methods)
def speak_to_jason():
    party_name = ""
    party_name_found = False
    answer = ""
    
    if request.is_json:
            data = request.get_json()
            party_name = data.get('party_name', '').strip().lower()
            party_name_found = len(party_name)>0
            speak = data.get('speak', '').strip().lower()
            print(request.headers)
            answer = request.headers.get('Authorization', '').strip().lower()
            answer = speak + " " + answer
    print(f"answer: {answer}")
    
    level:Level = levels[L.THE_THRONE_ROOM]
    next_level:Level = levels[L.THE_CROWN]
    level_response = build_answer_response(level, next_level, answer, party_name)
    response:Response = execute_level(level.name, level.get_failed_request_info(), 'GET', request.method, party_name_found, party_name,level_response)
    
    response_data = response.get_json()
    
    if response_data.get('level_completed'):
        level_info:dict = response_data['level_info']
        level_info.update({'answer_response':'HOLY FUCK! WHO SAID THAT?!'})
        level_info.update({'description':'JaSON looks around at the others - clearly affected by your telepathic powers. Good. Goooooo- well, better just read what is actually going on inside his HEAD...er...'})
        level_info.update({'next_level':'It seems like JaSON is hiding this inside his HEAD.'})
        response = jsonify(response_data)
        response.headers['JaSONs inner voice'] = 'He will never realise that I am hiding it behind my back hehe. I just have to keep playing stupid writle Wrason.'
        response.headers['The CRUDe Crown'] = next_level.directions
    
    return response


@app.route(R.THE_THRONE.value, methods=all_methods)
def the_throne_room():
    party_name = ""
    if request.is_json:
        data = request.get_json()
        party_name = data.get('party_name', '').strip().lower()
    party_name_found = len(party_name) > 0
    
    level:Level = levels[L.THE_THRONE_ROOM]
    response = execute_level(level.name,level.get_failed_request_info(), 'GET', request.method, party_name_found, party_name, level.get_welcome_info())
    return response

#LEVEL 4: THE GATE
@app.route(R.THE_GATE_OPEN.value, methods=all_methods)
def the_gate_open():
    party_name = ""
    answer = ""
    if request.is_json:
        data = request.get_json()
        party_name = data.get('party_name', '').strip().lower()
        answer = data.get('answer','').strip().lower()
    party_name_found = len(party_name) > 0
    
    level:Level = levels[L.THE_GATE]
    next_level:Level = levels[L.THE_THRONE_ROOM]
    level_response = build_answer_response(level, next_level, answer, party_name)
    response = execute_level(level.name,level.get_failed_request_info(), 'DELETE', request.method, party_name_found, party_name,level_response)
    return response

@app.route(R.THE_GATE.value, methods=all_methods)
def the_gate_arrival(party_name:str):
    party_name = party_name.strip().lower()
    party_name_found = len(party_name) > 0
    
    level:Level = levels[L.THE_GATE]
    response = execute_level(level.name,level.get_failed_request_info(), 'GET', request.method, party_name_found, party_name, level.get_welcome_info())
    return response

#LEVEL 3: THE GIT MONSTER
@app.route(R.STUN_THE_GIT_MONSTER.value, methods=all_methods) #'/the_git_monster/<string:team_name>/<string:answer>'
def stun_the_git_monster(party_name:str, answerA:str, answerB:str, answerC:str, answerD:str):
    party_name = party_name.strip().lower()
    party_name_found = len(party_name) > 0
    answer = answerA.strip().lower()
    answer += answerB.strip().lower()
    answer += answerC.strip().lower()
    answer += answerD.strip().lower()

    level:Level = levels[L.THE_MONSTER]
    next_level:Level = levels[L.THE_GATE]
    level_response = build_answer_response(level, next_level, answer, party_name)
    response = execute_level(level.name,level.get_failed_request_info(), 'PUT', request.method, party_name_found, party_name,level_response)
    return response

@app.route(R.MEET_THE_GIT_MONSTER.value, methods=all_methods) #'/the_git_monster/<string:team_name>'
def meet_the_git_monster(party_name:str):
    party_name = party_name.strip().lower()
    party_name_found = len(party_name) > 0
    
    level:Level = levels[L.THE_MONSTER]
    response = execute_level(level.name,level.get_failed_request_info(), 'GET', request.method, party_name_found, party_name, level.get_welcome_info())
    return response

#LEVEL 2: THE TEST
@app.route(R.THE_TEST_ANSWER.value, methods=all_methods) #/the_test/<string:party_name>/<string:answer>
def the_test_answer(party_name:str, answer:int):
    party_name = party_name.strip().lower()
    party_name_found = len(party_name) > 0
    
    level:Level = levels[L.THE_TEST]
    next_level:Level = levels[L.THE_MONSTER]
    level_response = build_answer_response(level, next_level, answer, party_name)
    response = execute_level(level.name,level.get_failed_request_info(), 'POST', request.method, party_name_found, party_name,level_response)
    return response

@app.route(R.THE_TEST_BEGINS.value, methods=all_methods) #'/the_test/<string:party_name>'
def the_test(party_name:str):
    party_name = party_name.strip().lower()
    party_name_found = len(party_name) > 0
    
    level:Level = levels[L.THE_TEST]
    
    response = execute_level(level.name,level.get_failed_request_info(), 'GET', request.method, party_name_found, party_name, level.get_welcome_info())
    return response
    
#LEVEL 1: REGISTER
@app.route(R.REGISTER.value, methods=all_methods)
def register():
    """This method executes a little different to ensure that the team is registered

    Returns:
        _type_: _description_
    """
    
    request_report = {
        'status_code':StatusCode.BAD_REQUEST.value, #assume failure
        'message':'Seems like we (or you?) broke the registation system. Lets try that again - or talk to a TA!'
    }
    
    level:Level = levels[L.REGISTRATION]
    if request.method != 'POST':
        request_report.update({'message':f'You must work on your METHODology... {level.quest + " " + level.hint}'})
        return request_report
    request_report.update({'valid_method':True})
    
    #check form
    if 'party' not in request.form:
        request_report.update({'message':f'Looks like your are out of shape! Or... as they say in Danish... {level.quest + " " + level.hint}'})
        return request_report
    
    #check party name
    party = request.form['party'].strip().lower()
    is_empty = len(party) == 0
    if is_empty:
        request_report.update({'message':f'Try with more characters than None and thin air. {level.quest + " " + level.hint}'})
        return request_report
    #a bit of name cleaning - for everyones sake
    party.replace(" ", "-space-")
    party.replace("/", "-dash-")
    party.replace(".", "-dot-")
    party.replace("@", "-at-")
    
    request_report.update({'party_found':True})
    request_report.update({'party':party})
    
    #check if party exists
    in_db  = get_game_db().get_team(party)
    if in_db:
        request_report.update({'is_registered':True})
        request_report.update({'message':f'It looks like your team is already registered? Try with another name or return to your quest. {level.quest + " " + level.hint}'})
        return request_report
    request_report.update({'party_is_registered':True})
    
    #register team
    get_game_db().store_team(party)
    
    #make success response
    next_level:Level = levels[L.THE_TEST]
    game_data = level.get_victory_info(party, next_level.directions)
    response = {'request_report':request_report, 'game_info':game_data}
    
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(response) #send as json
    
    #redirect to leader board
    return redirect(url_for('index', party_name=request_report['party'], new_party = True))

#HOME AND LEADERBOARD
@app.route(R.LEADERBOARD.value)
def index(party_name="", new_party=False):
    party_name = request.args.get('party_name', "")
    new_party = request.args.get('new_party', False)
    data = None
    
    if new_party:
        level:Level = levels[L.REGISTRATION]
        next_level:Level = levels[L.THE_TEST]
        data = level.get_victory_info(party_name, next_level.directions)

    return render_template('the_game.html', game_data=data, new_party = new_party)

#DIRECT DB REQUESTS
@app.route(R.GET_ALL_TEAMS.value)
def get_all_teams():
    teams = get_game_db().all_teams()
    teams_dict = [get_game_db().convert_team_to_json(team) for team in teams]
    return jsonify(teams_dict)

def get_game_db() -> QuestDB:
    """
    Retrieves the QuestDB instance from the global context (g) 
    or creates a new instance if it doesn't exist.

    Returns:
        QuestDB: The QuestDB instance.
    """
    db_instance = getattr(g, '_database', None)
    if db_instance is None:
        db_instance = g._database = QuestDB()
    return db_instance

#RUN AND TEARDOWN
@app.teardown_appcontext
def close_connection(_exception):
    """Close the database, when Flask exits.

    Args:
        _exception (_type_): not used
    """
    db_instance = getattr(g, '_database', None)
    if db_instance is not None:
        db_instance.close()

if __name__ == "__main__":
    app.run(debug=True)
