"""
This module contains a simple Flask application with route handling.
"""
from flask import Flask, request, jsonify, g, redirect, url_for, render_template, redirect

# from game.level import Level, LevelEnum as L
# from game.routes import Route as R
# from game.status_code import StatusCode
# import game.response_builder as RB

from game import level_builder as LB

from game.level import Level, LevelEnum as L
from game.routes import Route as R

from quest_db import QuestDB

#import game.response_builder as RB
import game.request_handler as RH
from game.status_code import StatusCode

app = Flask(__name__)



register_level:Level = LB.createRegisterLevel()
the_test_level:Level = LB.createTheTestLevel()
the_monster_level:Level = LB.createTheGitLevel()
the_gate_level:Level = LB.createGateLevel()
the_throne_level:Level = LB.createThroneLevel()
the_crown_level:Level = LB.createCrownLevel()
game_over:Level = LB.GameOverLevel()

handel_the_test_begins = { 'level':the_test_level,'next_level': None,'target_method':'GET','params_parser': RH.get_params_from_path, 'level_responder': RH.create_level_welcome_response}
handel_the_test_answer = { 'level':the_test_level,'next_level': the_monster_level,'target_method':'POST','params_parser': RH.get_params_from_path, 'level_responder': RH.create_level_answer_response}
handel_meet_the_monster = { 'level':the_monster_level,'next_level': None,'target_method':'GET','params_parser': RH.get_params_from_path, 'level_responder': RH.create_level_welcome_response}
handel_stun_the_monster = { 'level':the_monster_level,'next_level': the_gate_level,'target_method':'PUT','params_parser': RH.get_params_from_path, 'level_responder': RH.create_level_answer_response}
handel_the_gate = { 'level':the_gate_level,'next_level': None,'target_method':'GET','params_parser': RH.get_params_from_path, 'level_responder': RH.create_level_welcome_response}
handel_the_gate_open = { 'level':the_gate_level,'next_level': the_throne_level,'target_method':'DELETE','params_parser': RH.get_params_from_json_body, 'level_responder': RH.create_level_answer_response}
handel_the_throne_room = { 'level':the_throne_level,'next_level': None,'target_method':'GET','params_parser': RH.get_params_from_json_body, 'level_responder': RH.create_level_welcome_response}

r_funcs = {
        R.THE_TEST_BEGINS.value : handel_the_test_begins,
        R.THE_TEST_ANSWER.value : handel_the_test_answer,
        R.MEET_THE_GIT_MONSTER.value:handel_meet_the_monster,
        R.STUN_THE_GIT_MONSTER.value:handel_stun_the_monster,
        R.THE_GATE.value:handel_the_gate,
        R.THE_GATE_OPEN.value:handel_the_gate_open,
        R.THE_THRONE.value:handel_the_throne_room
    }

return_response = {
    'application/json' : lambda resp : jsonify(resp),
}

#LEVEL ROUTE HANDLER
@app.route('/<level>', defaults={'username': None, 'answers': []}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<level>/<string:username>', defaults={'answers': []}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<level>/<string:username>/<path:answers>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def level_routes_handler(level, username, answers):
    """Handle dynamic routes"""
    
    route = RH.rebuild_route(level, username, *answers)
    if route in r_funcs:
        #set default response
        level:Level = r_funcs[route].get('level',None)
        response = RH.create_default_response(level)
        
        # Retrieve X-secret-key from request headers
        secret_key = request.headers.get('X-secret-key', None)
        accepts = request.headers.get('Accept', None)
        
        print(f"SECRET KEY : {secret_key}, ACCEPTS: {accepts}")
        if not secret_key:
            response.update({'request_status': StatusCode.UNAUTHORIZED.value, 'error': 'Missing X-secret-key'})
            return return_response.get(accepts, lambda resp: render_template('level.html', level=resp))(response)
            #return jsonify(response)
            #if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            #    return jsonify(response)
            #return render_template('level.html', level=response)
        
        #get vars for request validation
        params_parser:callable = r_funcs[route].get('params_parser', None)
        params = params_parser(request)
        username = params.get('username','')
        username_registered = get_game_db().get_team(username) is not None
        
        #build request report
        target_method = r_funcs[route].get('target_method','')
        request_report = RH.validate_request(request, target_method, username, username_registered)
        response['request_report'] = request_report
        method_accepted = request_report['method_validation']['accepted']
        user_validated = request_report['user_validation']['accepted']
        if not(method_accepted and user_validated):
            return return_response.get(accepts, lambda resp: render_template('level.html', level=resp))(response)
            if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:   
                return jsonify(response)
            return render_template('level.html', level=response)
        response.update({'request_status':StatusCode.ACCEPTED.value}) #upgrades status to indicate method and username is handled correct
        
        #build level response
        level_responder:callable = r_funcs[route].get('level_responder','')
        next_level:Level = r_funcs[route].get('next_level',None)
        answer = r_funcs[route].get('answers','')
        level_info = level_responder(level = level, next_level=next_level, answer= answer, username=username)
        response.update({'level_info':level_info})
        
        #check if level completed
        answer_accepted = level_info.get('answer_accepted','')
        if answer_accepted:
            response.update({'request_accepted':True})
            response.update({'request_status':StatusCode.OK.value})
        
        return return_response.get(accepts, lambda resp: render_template('level.html', level=resp))(response)
        
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:   
            return jsonify(response)
        return render_template('level.html', level=response)
    return "Route not found. Seems like you have moved out of the playingfield?", 404 #big failure

@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username'].strip().lower()
            if username and get_game_db().get_team(username) is None:
                get_game_db().store_team(username)
                game_data = the_test_level.get_victory_info(username, the_test_level.directions)
                if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
                    return jsonify(game_data) #send as json
                return redirect(url_for('index', username=username, new_party = True))
            return redirect(url_for('index', registration_message="Username not found or already registered"))
    return redirect(url_for('index', registration_message="Did not call with POST method"))

#HOME AND LEADERBOARD
@app.route(R.LEADERBOARD.value)
def index(username="", new_party=False, registration_message=""):
    username = request.args.get('username', "")
    registration_message = request.args.get('registration_message', "")
    new_party = request.args.get('new_party', False)
    
    data = None
    
    if new_party:
        level:Level = LB.createRegisterLevel()
        next_level:Level = LB.createTheTestLevel()
        data = level.get_victory_info(username, next_level.directions)

    return render_template('the_game.html', game_data=data, new_party = new_party, reg_msg = registration_message)

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