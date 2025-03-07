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

r_funcs = {
        R.THE_TEST_BEGINS.value : { 'level':the_test_level,'next_level': None,'target_method':'GET'},
        R.THE_TEST_ANSWER.value : { 'level':the_test_level,'next_level': the_monster_level,'target_method':'POST'},
        R.MEET_THE_GIT_MONSTER.value: { 'level':the_monster_level,'next_level': None,'target_method':'GET'},
        R.STUN_THE_GIT_MONSTER.value: { 'level':the_monster_level,'next_level': the_gate_level,'target_method':'PUT'},
        R.THE_GATE.value: { 'level':the_gate_level,'next_level': None,'target_method':'GET'},
        R.THE_GATE_OPEN.value: { 'level':the_gate_level,'next_level': the_throne_level,'target_method':'DELETE'},
        R.THE_THRONE.value: { 'level':the_throne_level,'next_level': None,'target_method':'GET'}
    }

return_response = {
    'application/json' : jsonify,
}

def rebuild_route(level, party_name=None, *answers):
    route = level
    if party_name:
        route = route + "/<string:username>"
        if answers:
            for a in range(0, len(answers)):
                route = route + f"/<string:answer{a}>"
    return route

#LEVEL ROUTE HANDLER
@app.route('/<level>', defaults={'username': None, 'answers': []}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<level>/<string:username>', defaults={'answers': []}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<level>/<string:username>/<path:answers>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def level_routes_handler(level, username, answers):
    """Handle dynamic routes"""
    
    route = rebuild_route(level, username, *answers)
    if route in r_funcs:
        #set default response
        level:Level = r_funcs[route].get('level',None)
        failed_request_level_response = level.get_failed_request_info()
        response = {'request_status':StatusCode.BAD_REQUEST.value,
                'level_info': failed_request_level_response}
        
        #build request report
        target_method = r_funcs[route].get('target_method','')
        if not request.method == target_method:
            response.update({'request_status': StatusCode.UNAUTHORIZED.value, 'error': 'You must work on the METHODology.'})
            return jsonify(response), 404 #big failure
        response.update({'method_status': 'accepted'})
        
        # Retrieve X-secret-key from request headers
        secret_key = request.headers.get('X-secret-key', '').strip().lower()
        user_validated = secret_key and get_game_db().get_team(secret_key)
        if not user_validated:
            response.update({'request_status': StatusCode.UNAUTHORIZED.value, 'error': 'Missing the secret key ingredient X'})
            return jsonify(response), 404 #big failure
        response.update({'secret-key': 'accepted'})
        response.update({'request_status':StatusCode.ACCEPTED.value}) #upgrades status to indicate method and username is handled correct
        
        # Check if the request has data as JSON, path params, or form
        request_data = {}
        if request.is_json:
            request_data = request.get_json()
        elif request.args:
            request_data = request.args.to_dict()
        elif request.form:
            request_data = request.form.to_dict()
        else:
            request_data = {}
        
        #build level response
        next_level:Level = r_funcs[route].get('next_level',None)
        answer = request_data.get('answers','')
        level_info = level.level_report(username, answer, request.method, user_validated, next_level)
        response.update({'level_info':level_info})
        
        #check if level completed
        answer_accepted = level_info.get('answer_accepted','')
        if answer_accepted:
            response.update({'request_accepted':True})
            response.update({'request_status':StatusCode.OK.value})
        
        accepts = request.headers.get('Accept', None)
        return return_response.get(accepts, lambda resp: render_template('level.html', level=resp))(response)
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