from game.level import Level, LevelEnum as L
import game.level_builder as level_builder
from game.routes import Route as R
from game.status_code import StatusCode

import game.response_builder as RB

from quest_db import QuestDB
from flask import Flask, render_template, redirect, url_for, request, g, abort, jsonify, Response

app = Flask(__name__)

levels = {
    L.REGISTER: level_builder.createRegisterLevel(),
    L.THE_TEST: level_builder.createTheTestLevel(),
    L.THE_GIT_MONSTER : level_builder.createTheGitLevel(),
    L.THE_GATE : level_builder.createGateLevel(),
    L.THE_THRONE_ROOM : level_builder.createThroneLevel(),
    L.THE_CROWN : level_builder.createCrownLevel()
}

all_methods = ['GET', 'POST', 'PUT', 'DELETE']

def execute_level(level:Level, next_level:Level, 
                  target_method, method, 
                  party_data_found, party, 
                  answer, request_is_answer):
    """
    Execute a level by validating method, team name, (and answer for answer_routes) up against a given levels requirements.

    Args:
        level (Level): _description_
        next_level (Level): _description_
        target_method (_type_): _description_
        method (_type_): _description_
        party_data_found (_type_): _description_
        party (_type_): _description_
        answer (_type_): _description_
        request_is_answer (_type_): _description_

    Returns:
        _type_: a JSON response to the requester.
    """
    method_response = RB.create_method_response(method, target_method)
    if not method_response['success']:
        return jsonify(method_response)
    
    party_registered = False
    if party_data_found:
        party_registered = get_db().get_team(party) is not None
    data_response = RB.create_data_response(party_data_found, party, party_registered)
    if not data_response['success']:
        return jsonify(data_response)
    
    if request_is_answer:
        answer_response = RB.create_answer_response(level, next_level, answer, party, data_response['success'], method_response['success'])
        if answer_response['success']:
            get_db().update_score(party, 1)
        return jsonify(answer_response)
    return jsonify(RB.create_level_welcome_response(level))

#LEVEL 6: THE CROWN
@app.route(R.THE_THRONE.value, methods=all_methods)
def the_crown():
    party = ""
    if request.is_json:
        data = request.get_json()
        party = data.get('party', '').strip().lower()
    party_not_empty = len(party) > 0
    
    response = execute_level(levels[L.THE_THRONE_ROOM], levels[L.THE_CROWN], 
                                'PUT', request.method, party_not_empty, 
                                party, None, False)
    return response

#LEVEL 5: THE THRONE ROOM
@app.route(R.THE_THRONE.value, methods=all_methods)
def the_throne_room():
    party = ""
    if request.is_json:
        data = request.get_json()
        party = data.get('party', '').strip().lower()
    party_not_empty = len(party) > 0
    
    response = execute_level(levels[L.THE_THRONE_ROOM], levels[L.THE_CROWN], 
                                'GET', request.method, party_not_empty, 
                                party, None, False)
    return response

#LEVEL 4: THE GATE
@app.route(R.THE_GATE_OPEN.value, methods=all_methods)
def the_gate_open():
    party = ""
    answer = ""
    if request.is_json:
        data = request.get_json()
        party = data.get('party', '').strip().lower()
        answer = data.get('answer','').strip().lower()
    party_not_empty = len(party) > 0
    
    response = execute_level(levels[L.THE_GATE], levels[L.THE_THRONE_ROOM], 
                             'DELETE', request.method, 
                             party_not_empty, party, 
                             answer, True)
    return response

@app.route(R.THE_GATE.value, methods=all_methods)
def the_gate_arrival(party:str):
    party = party.strip().lower()
    party_not_empty = len(party) > 0
    response = execute_level(levels[L.THE_GATE], levels[L.THE_THRONE_ROOM], 
                                'GET', request.method, party_not_empty, 
                                party, None, False)
    return response

#LEVEL 3: THE GIT MONSTER
@app.route(R.STUN_THE_GIT_MONSTER.value, methods=all_methods) #'/the_git_monster/<string:team_name>/<string:spell>'
def stun_the_git_monster(party:str, spell:str):
    party = party.strip().lower()
    party_not_empty = len(party) > 0
    spell = spell.strip().lower()
    spell = spell.replace("20%", " ")

    response = execute_level(levels[L.THE_GIT_MONSTER], levels[L.THE_GATE], 
                             'PUT', request.method, 
                             party_not_empty, party, 
                             spell, True)
    return response

@app.route(R.MEET_THE_GIT_MONSTER.value, methods=all_methods) #'/the_git_monster/<string:team_name>'
def meet_the_git_monster(party:str):
    party = party.strip().lower()
    party_not_empty = len(party) > 0
    
    response = execute_level(levels[L.THE_GIT_MONSTER], levels[L.THE_GIT_MONSTER], 
                             'GET', request.method, 
                             party_not_empty, party, 
                             None, False)
    return response

#LEVEL 2: THE TEST
@app.route(R.THE_TEST_ANSWER.value, methods=all_methods) #/the_test/<string:party>/<string:answer>
def the_test_answer(party:str, answer:int):
    party = party.strip().lower()
    party_not_empty = len(party) > 0
    
    response = execute_level(levels[L.THE_TEST], levels[L.THE_GIT_MONSTER], 
                             'POST', request.method, 
                             party_not_empty, party, 
                             answer, True)
    return response
    
@app.route(R.THE_TEST_BEGINS.value, methods=all_methods) #'/the_test/<string:party>'
def the_test(party:str):
    party = party.strip().lower()
    party_not_empty = len(party) > 0
    
    response = execute_level(levels[L.THE_TEST], levels[L.THE_GIT_MONSTER], 
                             'GET', request.method, 
                             party_not_empty, party, 
                             None, False)
    return response
    
#LEVEL 1: REGISTER
@app.route(R.REGISTER.value, methods=all_methods)
def register():
    """This method executes a little different to ensure that the team is registered

    Returns:
        _type_: _description_
    """
    party = ""
    party_in_form = False
    try:
        party_in_form = 'party' in request.form
        party = request.form['party'].strip().lower()
    except:
        print("no party in form")
    
    data_response = RB.create_data_response(party_in_form, party, get_db())
    if data_response['success']:
        data_response.update({'message':'Seems like this party is already registered?'})
        return jsonify(data_response)
    
    method_response = RB.create_method_response(request.method, 'POST')
    if not method_response['success']:
        return jsonify(method_response)
    
    #SUCCESS
    level:Level = levels[L.REGISTER]
    next_level:Level = levels[L.THE_TEST]
    success_response = RB.create_answer_response(level, next_level, True, data_response['party'])
    
    get_db().store_team(data_response['party']) #register party
    
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        #send as json
        return jsonify(success_response)
    #redirect to leader board
    return redirect(url_for('index', message=success_response['message'], new_party = True))

@app.route(R.HOME.value)
def index(message="", new_party=False):
    message = request.args.get('message', "We are looking forward to follow your adventure.")
    new_party = request.args.get('new_party', False)
    return render_template('index.html', game_feedback=message, registration_complete = new_party)

@app.route(R.GET_ALL_TEAMS.value)
def get_all_teams():
    teams = get_db().all_teams()
    teams_dict = [get_db().convert_team_to_json(team) for team in teams]
    return jsonify(teams_dict)

def get_db() -> QuestDB:
    """
    Retrieves the GreetingsDB instance from the global context (g) 
    or creates a new instance if it doesn't exist.

    Returns:
        GreetingsDB: The GreetingsDB instance.
    """
    db_instance = getattr(g, '_database', None)
    if db_instance is None:
        db_instance = g._database = QuestDB()
    return db_instance

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
