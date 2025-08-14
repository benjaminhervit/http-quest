from flask import request, jsonify, Request

import app.blueprints.quests.quest_factory as Q_factory
from app.blueprints.quests.identify_yourself.handlers import get_handlers
from app.request_handler import RequestHandler
from app.blueprints.quests import bp
# from app.quest import QuestData
# from app.utils import is_browser_request, respond
# import app.utils.parser_utils as Parsers

# from app.extensions import db
# from app.models.user import User
# from app.enums import StatusCode
# from app.errors import ParsingError, ValidationError, GameError
# from blueprints.quests import content_generator

@bp.route('/identify_yourself', methods=['GET', 'POST'])
def register():
    quest = Q_factory.get_identify_yourself_quest()
    handlers = get_handlers()
    valid_methods = ['GET', 'POST']
    return RequestHandler.execute(request, quest, handlers, valid_methods)
        # try:
    #     #  Setup
    #     quest = Q_factory.get_identify_yourself_quest()
    #     req_from_browser = is_browser_request(request)
    #     content = content_generator.create_start_content(quest)

    #     #  handle GET
    #     if request.method == 'GET':
    #         return respond(content, StatusCode.OK.value, req_from_browser)

    #     #  Handle POST
    #     username = Parsers.get_field_from_request_data(request,
    #                                                    'authorization',
    #                                                    Parsers.get_headers)
    #     if not username:
    #         raise ParsingError('Found no username in form?',
    #                            StatusCode.BAD_REQUEST.value)
    #     if not User.user_exists(username):
    #         raise ValidationError((f'Username {username} does not exists'
    #                                'go to /auth/register to sign up.'),
    #                               StatusCode.BAD_REQUEST.value)

    #     #  build response content
    #     content = content_generator.create_completed_content(quest)
    #     placeholder_map = {'[HERO]': username}
    #     content = content_generator.replace_placeholders(content,
    #                                                    placeholder_map)
    #     return respond(content, StatusCode.OK.value, req_from_browser)
    
    # # error handling
    # except ParsingError as e:
    #     print("DOWN IN PARSING!")
    #     content = content_generator.create_error_msg(str(e), 
    #                                                'ParsingError', e.code)
    #     return respond(content, StatusCode.SERVER_ERROR.value, req_from_browser,
    #                    html='error_message.html')
    
    # except ValidationError as e:
    #     content = content_generator.create_error_msg(str(e),
    #                                                'ValidationError', e.code)
    #     return respond(content, e.code, req_from_browser,
    #                    html='error_message.html')
    
    # except GameError as e:
    #     content = content_generator.create_error_msg(str(e),
    #                                                'GameError', e.code)
    #     return respond(content, e.code, req_from_browser,
    #                    html='error_message.html')