from enum import Enum
#inspired by https://www.w3.org/Protocols/HTTP/HTRESP.html
class Route(Enum):
    LEADERBOARD = "/" #GET
    REGISTER = "/register" #POST FORM
    THE_TEST_BEGINS = "/the_test/<string:party_name>" #GET PATH
    THE_TEST_ANSWER = "/the_test/<string:party_name>/<int:answer>" #POST PATH
    MEET_THE_GIT_MONSTER = '/the_monster/<string:party_name>' #GET PATH
    STUN_THE_GIT_MONSTER = '/the_monster/<string:party_name>/<string:a_b_c_d>' #POST PATH
    THE_GATE = '/the_gate/<string:party_name>' #GET PATH POST JSON
    THE_GATE_OPEN = '/the_gate' #POST JSON
    THE_GIT_AWAY = '/open/the_gate/git_away_fast' #POST JSON
    THE_THRONE = '/the_throne_room' #GET JSON
    READ_JASONS_MIND = '/read_jasons_mind' #POST JSON
    THE_CROWN = '/the_crude_crown' #POST JSON HEAD
    
    GET_ALL_TEAMS = '/all_teams'