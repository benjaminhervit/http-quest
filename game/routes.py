from enum import Enum
#inspired by https://www.w3.org/Protocols/HTTP/HTRESP.html
class Route(Enum):
    LEADERBOARD = "/leaderboard" #GET
    REGISTER = "/register" #POST FORM
    THE_TEST_BEGINS = "/the_test/<string:party>" #GET PATH
    THE_TEST_ANSWER = "/the_test/<string:party>/<int:answer>" #POST PATH
    MEET_THE_GIT_MONSTER = '/the_git_monster/<string:party>' #GET PATH
    STUN_THE_GIT_MONSTER = '/the_git_monster/<string:party>/<string:spell>' #POST PATH
    THE_GATE = '/the_gate/<string:party>' #GET PATH POST JSON
    THE_GATE_OPEN = '/the_gate' #POST JSON
    THE_GIT_AWAY = '/open/the_gate/git_away_fast' #POST JSON
    THE_THRONE = '/the_throne_room' #GET JSON
    SPEAK_TO_JASON = '/speak_to_jason', #POST JSON
    THE_CROWN = '/the_crown', #POST JSON HEAD
    
    GET_ALL_TEAMS = '/all_teams'