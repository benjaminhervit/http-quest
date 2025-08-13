from flask import request, jsonify
from app.utils import respond, is_browser_request
import app.utils.parser_utils as Parsers

import app.quest_factory as Q_factory
from app.errors import ParsingError
from app.enums import StatusCode
from app.quest import QuestData
from app.blueprints.quests import bp
import app.blueprints.quests.content_factory as content_factory


@bp.route('/hire_jason', methods=['GET', 'POST'])
def hire_json():
    quest = Q_factory.get_hire_jason_quest()
    content = content_factory.create_locked_content(quest)

    if request.method == 'GET':
        content = content_factory.create_start_content(quest)

    if request.method == 'POST':
        hired = Parsers.get_field_from_request_data(request, 'jason',
                                                    Parsers.get_json)
        if hired != 'hired':
            return "FUCK!"

    return respond(content, StatusCode.ACCEPTED.value,
                   is_browser_request(request))
    return jsonify(content)
    if request.method == 'GET':
        return "JUST ARRIVED"
    
    return "SOMETHING WITH POST!"