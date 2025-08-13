from flask import request, jsonify
from app.utils import respond, is_browser_request
import app.utils.parser_utils as Parsers

from app.errors import ParsingError
from app.enums import StatusCode
from app.quest import QuestData
from app.blueprints.quests import bp
import app.blueprints.quests.content_factory as content_factory

quest = QuestData(
    title="Hire Jason",
    locked="I am sorry hero but I cannot allow you in just yet.",
    start_message="""
    Hello [HERO]! Pleased to meet you! I am... who gives a sh- I got a great squire for you!
    Meet: Jason! Jason can do all sorts of tricks for you - but you need to speak to him in his own language.
    """,
    quest="POST jason:hired in Jasons mother toungue also known as... yes... json...",
    completed="ALRIGHTY OH! Jasons screams and charges ahead. He does not really seem to care what orders he gets...",
    next_path="TBD"
)

@bp.route('/hire_jason', methods=['GET', 'POST'])
def hire_json():
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