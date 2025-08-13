from flask import request

import app.quest_factory as Q_factory
from app.utils import is_browser_request, respond
from app.enums import StatusCode
from app.blueprints.quests import bp
from app.blueprints.quests import content_factory
from app.quest import QuestData

@bp.route("/start", methods=['GET'])
@bp.route("/start" + '/<username>', methods=['GET'])
def start(username=None):
    quest = Q_factory.get_welcome_quest()
    content = content_factory.create_locked_content(quest)
    if username:
        placeholder_map = {'[HERO]': username}
        raw_content = content_factory.create_completed_content(quest)
        content = content_factory.replace_placeholders(raw_content,
                                                       placeholder_map)
    else:
        content = content_factory.create_start_content(quest)
        
    return_as_html = is_browser_request(req=request)
    return respond(content, StatusCode.OK.value, return_as_html)
