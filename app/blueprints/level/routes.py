from flask import request
from app.blueprints.level import bp
from app.game.levels import level_factory as LF

# GM = GameManager()
# ReqMgmt = RequestManager()
levels = LF.get_all_levels()

@bp.route('/welcome')
def welcome():
    level = LF.create_register_level()
    # level = WelcomeLevel()
    # if not ReqMgmt.request_is_valid(request):
    #     return ReqMgmt.create_bad_request_response(level)
    # player_actions = ReqMgmt.get_player_actions(request)
    # response = GM.run_level(level, player_actions)
    # return response
    return level.get_welcome_info()