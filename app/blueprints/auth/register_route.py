from flask import request, jsonify, Request

from app.blueprints.auth import bp
from app.utils import is_browser_request, respond, get_form_field

from app.extensions import db
from app.models.user import User
from app.enums import StatusCode, ContentKeys as CK
from app.errors import ParsingError, ValidationError, GameError
from app.blueprints.quests import content_factory

quest = {
    CK.TITLE.value: "Registration",
    CK.START_MESSAGE.value: ("""To begin the quest, you must tell us your
                                 name,so that we can follow you on y
                                 our adventures."""),
    CK.QUEST.value: ("""FORM username:your_name and POST to auth/register
                      or... you know... just use the form below?"""),
    CK.COMPLETED.value: ("""
                         Thank you [HERO]! Now, you are ready!",
                         Finally, someone with a heroic name as [HERO]
                         cannot fail! Move on! 
                         REEEEEMEMBEEEER to aaaalwaaaayyyyys 
                         keep your name in your head at all times.
                         """),
    CK.NEXT_PATH.value: ("""
                         GET to /telekenisis as fast as you can.
                         This is a skill that you cannot 
                         ignore if you want to succeed!
                         """)
}

@bp.route('/register', methods=['GET', 'POST'])
def register():
    try:
        #  Setup
        req_from_browser = is_browser_request(request)
        content = content_factory.create_start_content(quest)

        #  handle GET
        if request.method == 'GET':
            return respond(content, StatusCode.OK.value, req_from_browser,
                           html='register.html')

        #  Handle POST
        #  data validation
        username = get_form_field(request, 'username')
        if not username:
            raise ParsingError('Found no username in form?',
                               StatusCode.BAD_REQUEST.value)
        if User.user_exists(username):
            raise ValidationError('Username already exists',
                                  StatusCode.BAD_REQUEST.value)
        #  add new user
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

        #  build response content
        content = content_factory.create_completed_content(quest)
        placeholder_map = {'[HERO]': username}
        content = content_factory.replace_placeholders(content,
                                                       placeholder_map)
        return respond(content, StatusCode.OK.value, req_from_browser)
    
    # error handling
    except ParsingError as e:
        print("DOWN IN PARSING!")
        content = content_factory.create_error_msg(str(e), 
                                                   'ParsingError', e.code)
        return respond(content, StatusCode.SERVER_ERROR.value, req_from_browser,
                       html='error_message.html')
    
    except ValidationError as e:
        content = content_factory.create_error_msg(str(e),
                                                   'ValidationError', e.code)
        return respond(content, e.code, req_from_browser,
                       html='error_message.html')
    
    except GameError as e:
        content = content_factory.create_error_msg(str(e),
                                                   'GameError', e.code)
        return respond(content, e.code, req_from_browser,
                       html='error_message.html')