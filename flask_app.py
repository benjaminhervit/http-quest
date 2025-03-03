"""
Creates a simpleminded CRUD/REST(?) based teaching game where the player must make the correct HTTP requests to advance in the game.
The intention is that the player will gain handson experience and understanding of the basic differences between GET, POST, DELETE, and PUT
and sending data as url args, forms and json.

Linke to HTTP status codeS: https://www.semrush.com/blog/http-status-codes/?g_network=g&g_keyword=&g_campaign=NE_SRCH_DSA_Blog_EN&g_acctid=503-093-2724&g_keywordid=dsa-2185834088336&g_adtype=search&g_adid=676326011189&g_campaignid=18350115241&g_adgroupid=159562815492&kw=&cmp=NE_SRCH_DSA_Blog_EN&label=dsa_pagefeed&Network=g&Device=c&utm_content=676326011189&kwid=dsa-2185834088336&cmpid=18350115241&agpid=159562815492&BU=Core&extid=180213783648&adpos=&gad_source=1&gclid=Cj0KCQiA_Yq-BhC9ARIsAA6fbAhAMfXrYRj1gYz9ygPuwKn-FmyHSa7Q9_1Mx8shw1ukmOzUoGzqr44aAt3fEALw_wcB

"""
from flask import Flask, render_template, redirect, url_for, request, g, abort, jsonify, Response
from quest_db import QuestDB
from enum import Enum

app = Flask(__name__)

error_msgs = {
    'no_team' : 'We do not recognize your team. Are you trying to jump ahead or do have troubles spelling your own name?',
    'level_error':'You cannot complete this level. Have you alrady completed it or did you end here by mistake?'
}

routes = {
    'the_test' : '/the_test',
    'the_answer' : '/the_answer/<int:answer>',
    'accept_quest': '/accept_the_quest', #FORM
    'git_monster' :'/stun_the_git_monster/<string:team_name>/<string:spell>',
    'the_gate_arrive':'/the_gate',
    'the_gate_open':'/open/the_gate/<string:team_name>/<string:secret_word>',
    'the_gate_git_away' : '/open/the_gate/git_away_fast',
    'the_throne' : '/the_throne_room',
    'jason' :'/speak_to_jason', #JSON
    'crown' : '/the_crown'
}

answers = {
    'the_answer' : 42,
    'accept_quest':'aw yeah',
    'git_monster':'add commit pull push',
    'gate_word' : 'mellon',
    'git_away_fast' : 'git_away_fast',
    'jason':f'Is it not obvious? You must PUT on {routes["crown"]} while in my language you announce: your first words for the world to hear as a ruler of CRUD.'
}

clues = {
    'the_test': f'First, you must answer me this: What is the meaning with the universe, life and everything? Now you must POST {routes["the_answer"]}',
    'accept_quest': f'Now, if you accept_the_quest, POST me an {answers["accept_quest"]}, your team_name, and the_answer at {routes["accept_quest"]}. \n FORM your words wisely.',
    'git_monster': f'To {routes["git_monster"]} you must PUT the four magic words pull commit add push in the right order. That should give you a 20% URL chance to escape.',
    'get_to_the_gate':f'Soon you GET to {routes["the_gate_arrive"]}',
    'the_gate_open':f'To {routes["the_gate_open"]} you must DELETE it using an old forgotten language: Speak friend and enter...',
    'git_away_fast':f'Better GET inside the {routes["the_gate_git_away"]} before the git monster catches up with you again.',
    'the_throne':f'GET to the {routes["the_throne"]} at the end of the hall.',
    'jason':f'You must {routes['jason']} in his native language and ask: what must i do?'
}

# THIS IS THE QUEST ROUTES

#1 - 2. A test to find those who are worthy
@app.route(routes['the_test'])
def the_test() -> str:
    return f'Great that you could GET here! {clues['the_test']}'

@app.route(routes['the_answer'], methods=['GET','POST'])
def the_answer(answer:int) -> str:
    if request.method == 'POST':
        if answer == 42:
            return f'That is correct! {clues["accept_quest"]}'
        return f'{routes['the_answer']} is not correct. A hitch hiker can help you. {clues["accept_quest"]}'
    if request.method == 'GET':
        return f'You have found the path but answers are not something you GET here. It is something you POST. {clues["accept_quest"]}'
    return f'You have found the path but you have not POSTed anything. {clues["accept_quest"]}'

#3. Where the group accepts the quest
@app.route(routes['accept_quest'], methods=['GET','DELETE','POST'])
def accept_the_quest() ->str:
    if request.method != 'POST':
        return f'You have found the path but you have not POSTed anything? {clues['accept_quest']}'
    
    has_group = 'team_name' in request.form
    has_universe_answer = 'answer' in request.form
    has_quest_answer = 'accept_the_quest' in request.form
    if not(has_group and has_universe_answer and has_quest_answer):
        return f"You are here but you do not want to tell me who you are or what the_answer is? {clues['accept_quest']}"
        
    quest_accepted = request.form['accept_the_quest'].lower()
    if quest_accepted != answers['accept_quest']:
        return f"You are here but do not wish to acccept the quest? {clues['accept_quest']}"
    
    try:
        answer = request.form['answer']
        answer = int(answer)
        if answer == answers['the_answer']:
            group = request.form['team_name']
            get_db().store_team(group)
            return f"Thank you, brave {group}! Your dangerous quest begins immediately as a git monster is approaching. You know by the growing stench of merge conflict. {clues['git_monster']} "
        return f"Come back with the right answer {group}. {clues['the_test']}"
    except ValueError:
        return f"You answer in a format that I do not understand, {group}. INTeresting..."

#4. Where the group PUTs the git monster down
@app.route(routes['git_monster'], methods=['GET', 'DELETE', 'POST','PUT'])
def the_git_monster(team_name:str,spell:str) -> str:
    errMessage = f'Whatever you tried - it is not working. {clues['git_monster']}'
    if request.method != 'PUT':
        return abort(405, errMessage)
    
    if not get_db().get_team(team_name):
        return abort(400, error_msgs['no_team'] + clues['git_monster'])
    
    if spell != answers['git_monster']:
        return abort(400, errMessage)
    
    if not get_db().update_level('git_monster'):
        return abort(400, f'{error_msgs['level_error']}. {clues["git_monster"]}' )
        
    get_db().update_score(team_name, 2)
    return f"""The git monster falls into a deep paralysis as you yell "git add . git commit -m "work!" git pull git push" -
        but you suspect it is only for a while, so you hurry on before it wakes up again. {clues["get_to_the_gate"]}"""
        
        
#5 - 6. where the group DELETEs the gate and GET away
@app.route(routes['the_gate_arrive'], methods=['GET'])
def the_gate():
    return f'Your path is blocked by a giant gate! There is only one thing to do. {clues['the_gate_open']}'

@app.route(routes['the_gate_open'], methods=['GET', 'DELETE', 'POST'])
def the_gate_open(team_name,secret_word:str)->str:
    if request.method == 'DELETE' and secret_word == answers['gate_word']:
        if get_db().update_level('the_gate_open'):
            get_db().update_score(team_name, 1)
            return f'As the gate deletes itself, you hear the git monster awakening again. {clues['git_away_fast']}'            
        return abort(400, f'{error_msgs["level_error"]} {clues['the_gate_open']}')
        
    if request.method == 'GET' and secret_word == answers['git_away_fast']:
        if get_db().update_level('git_away'):
            get_db().update_score(team_name, 1)
            return f"""You GET inside the gate just before the walls falls down and blocks the path behind you.
                    On the other side you hear the raging chaos of merge conflicts, branches, invalid paths, and wrong passwords banging against the solid rocks.
                    Luckily, you do not have to deal with that today. {clues['the_throne']}"""
        return f'You are too slow and are now stuck in merge conflicts. {clues["git_away_fast"]}'
    return abort(400, f"I don't know where you are getting at but maybe you should start deleting first or maybe there is something else wrong? {clues['git_away_fast']}")

#7 - 10. Where the group GET to the throne and PUT on the crown
@app.route(routes['the_throne'])
def the_throne_room():
    return f"""Inside {routes["the_throne"]} you see the legendary WoT throne and CRUD {routes['crown']}.
            Next to it stands some of its most renowned council members: HTML, CSS, SQL, Python, JS, Git, Venv, HTTP, and... someone called Jason? 
            They all start speaking on top of each other, making gesture towards the throne but it is impossible for you to understand any of it.
            Only Jason looks at you, silently but as if he knows something. {clues['jason']}"""
            
            
            #"""Now, standing in front of it there is only one thing left to do: PUT the /the_crown/on_your_team_name"""

# @app.route(routes['jason'], methods=['POST'])
# def jason():
#     if request.method == 'POST':
#         try:
#             content = request.to_json()
        
    
    

@app.route('/the_crown/<string:team_name>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def the_crown(team_name : str) -> str:
    #check if team_name exists. 
    if request.method == 'PUT':
        return 'Congratulations! You are now the master of CRUD and soon the ruler of WoT! Use your powers for the good... Do you wonder if this could have ended in a different way?'
    if request.method == 'POST':
        return 'You start POSTing about your accomplishment on all your social media too focused on getting the recognition and likes from your friends that you forget all about putting on the crown and the council silently hides it away until a more worthy ruler comes.'
    if request.method == 'DELETE':
        return 'in a moment of insanity you decide to throw away the crown! The WoT council gasps at your actions now looking at you with disbelief and discust. You wish you had DELETEd yourself instead.'
    return 'You GET the crown but fumble and drop it on the floor. The metallic sound echoes through the big, silent hall. One of the council members tries to choke a cough while another shift the weight from foot to foot... awkwaaaard... better try again.'

@app.route('/register_party')
def register_team():
    response = dict()
    if request.method == 'POST':
        if 'team' in request.form:
            team = request.form['team']
            if get_db().get_team(team):
                response.update({'success': False})
                response.update({'message': 'That team is already registered! REFRESH your name game or continue the quest where you left off!'})
                return jsonify(response)
            response.update({'success': True})
            response.update({'message':f"""Welcom to the leaderboard {team}! From here on, you are on your own. 
                    Use your skills to CRUD your way through the challenges. 
                    You choose your own weapons but you will need more than one.
                """})
            return jsonify(response)
    response.update({'success': False})
    response.update({'message': 'Wrong method or team value'})
    return jsonify(response)

@app.route('/all_teams')
def get_all_teams():
    teams = get_db().all_teams()
    teams_dict = [{'id':team[0],'team': team[1], 'score': team[2]} for team in teams]
    return jsonify(teams_dict)

@app.route("/")
def index() -> str:
    """The front page, where users can enter a greeting

    Returns:
        str: the generated page
    """
    get_db().store_team('test')
    return render_template("index.html", groups = get_db().all_teams(), tier2=4, tier3=6)

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
