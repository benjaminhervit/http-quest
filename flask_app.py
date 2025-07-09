"""
This module contains a simple Flask application with route handling.
"""
from flask import Flask, request, jsonify, g, redirect, url_for, render_template, current_app
from app.user_db.user_db import UserDatabase

from functools import partial
from app import create_app




#import game
# from game.quest_db import QuestDB
# from game import level_builder as LB
# from game.level import Level, exec_level_conclusion, exec_level_entry

# import game.request_handler as RH

from game.routes import Route as R

app = create_app()

# def get_game_db() -> QuestDB:
#     db_instance = getattr(g, '_database', None)
#     if db_instance is None:
#         db_instance = g._database = QuestDB()
#     return db_instance

# register_level:Level = LB.createRegisterLevel()
# the_test_level:Level = LB.createTheTestLevel()
# the_monster_level:Level = LB.createTheGitLevel()
# the_gate_level:Level = LB.createGateLevel()
# the_throne_level:Level = LB.createThroneLevel()
# the_crown_level:Level = LB.createCrownLevel()
# game_over:Level = LB.GameOverLevel()

# r_funcs = {
#         R.THE_TEST_BEGINS.value : partial(RH.handle_request, target_method='GET', 
#                                           level=the_test_level, next_level=None, level_response=exec_level_entry,
#                                           get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_path),
#         R.THE_TEST_ANSWER.value : partial(RH.handle_request, target_method='POST', 
#                                           level=the_test_level, next_level=the_monster_level, level_response=exec_level_conclusion,
#                                           get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_path),
#         R.MEET_THE_GIT_MONSTER.value : partial(RH.handle_request, target_method='GET', 
#                                           level=the_monster_level, next_level=None, level_response=exec_level_entry,
#                                           get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_path),
#         R.STUN_THE_GIT_MONSTER.value : partial(RH.handle_request, target_method='PUT', 
#                                           level=the_monster_level, next_level=the_gate_level, level_response=exec_level_conclusion,
#                                           get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_path),
#         R.THE_GATE.value : partial(RH.handle_request, target_method='GET', 
#                                         level=the_gate_level, next_level=None, level_response=exec_level_entry,
#                                         get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_path),
#         R.THE_GATE_OPEN.value : partial(RH.handle_request, target_method='DELETE', 
#                                         level=the_gate_level, next_level=the_throne_level, level_response=exec_level_conclusion,
#                                         get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_json_body),
#         R.THE_THRONE.value : partial(RH.handle_request, target_method='GET', 
#                                         level=the_gate_level, next_level=None, level_response=exec_level_entry,
#                                         get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_json_body),
#         R.THE_CROWN.value : partial(RH.handle_request, target_method='GET', 
#                                         level=the_gate_level, next_level=the_crown_level, level_response=exec_level_conclusion,
#                                         get_secret_key=RH.get_secret_key_from_path, get_data=RH.get_params_from_json_body)
#     }

# def rebuild_route(level, party_name=None, answers=None):
#     route = level
#     if party_name:
#         route = route + "/<string:username>"
#         if answers is not None:
#             ans_parts = answers.split('/')
#             print(ans_parts)
#             for a in range(0, len(ans_parts)):
#                 route = route + f"/<string:answer{a}>"
#     return route

# #LEVEL ROUTE HANDLER
# @app.route('/<level>', defaults={'username': None, 'answers': None}, methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route('/<level>/<string:username>', defaults={'answers': None}, methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route('/<level>/<string:username>/<path:answers>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def level_routes_handler(level, username, answers):
#     """Handle dynamic routes"""
#     print(f"answers:{answers}, type:{type(answers)}")
#     route = rebuild_route(level, username, answers)
#     print(f"route: {route}")
    
    
#     handler = r_funcs.get(route)
#     if handler:
#         return handler(req = request, db = get_game_db())
#     else:
#         return jsonify({"error": "Invalid request"}), 404

# @app.route('/register', methods=['POST'])
# def register_user():
#     if request.method == 'POST':
#         if 'username' in request.form:
#             username = request.form['username'].strip().lower()
#             if username and get_game_db().get_team(username) is None:
#                 get_game_db().store_team(username)
#                 game_data = the_test_level.get_victory_info(username, the_test_level.directions)
#                 if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
#                     return jsonify(game_data) #send as json
#                 return redirect(url_for('index', username=username, new_party = True))
#             return redirect(url_for('index', registration_message="Username not found or already registered"))
#     return redirect(url_for('index', registration_message="Did not call with POST method"))

#HOME AND LEADERBOARD
# @app.route(R.LEADERBOARD.value)
# def index(username="", new_party=False, registration_message=""):
#     username = request.args.get('username', "")
#     registration_message = request.args.get('registration_message', "")
#     new_party = request.args.get('new_party', False)
    
#     data = None
    
#     if new_party:
#         level:Level = LB.createRegisterLevel()
#         next_level:Level = LB.createTheTestLevel()
#         data = level.get_victory_info(username, next_level.directions)

#     return render_template('the_game.html', game_data=data, new_party = new_party, reg_msg = registration_message)

# #DIRECT DB REQUESTS
# @app.route(R.GET_ALL_TEAMS.value)
# def get_all_teams():
#     teams = get_game_db().all_teams()
#     teams_dict = [get_game_db().convert_team_to_json(team) for team in teams]
#     return jsonify(teams_dict)

#RUN AND TEARDOWN
# @app.teardown_appcontext
# def close_connection(_exception):
#     """Close the database, when Flask exits.

#     Args:
#         _exception (_type_): not used
#     """
#     db_instance = getattr(g, '_database', None)
#     if db_instance is not None:
#         db_instance.close()

# def get_db():
#     """Get database instance from Flask's application context"""
#     if 'db' not in g:
#         # Initialize your database here - this example assumes UserDatabase
#         g.db = UserDatabase(current_app)
#     return g.db

if __name__ == "__main__":
    app.run(debug=True)