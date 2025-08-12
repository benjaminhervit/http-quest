from flask import request, jsonify, redirect, url_for, session, render_template
import json

from app.utils import is_browser_request, respond
from app.enums import StatusCode, ContentKeys as CK
from app.blueprints.quests import bp
from app.blueprints.quests import content_factory

quest = {
    CK.TITLE.value: "Welcome",
    CK.START_MESSAGE.value: ["Welcome reQuest! An epic adventure to claim the CRUDe crown!",
                      "But before we begin, you must tell me who you are adventurer?"],
    CK.QUEST.value: ["Extend the path with /your_name"],
    CK.COMPLETED.value: ["What a pleasure to meet you [HERO]! Now, I believe in you! I do but... ",
                  "how should I put it... I prefer not to put all my trust in one hero?",
                  "Better 10 heroes on the roof than one in my pocket?",
                  "What I mean is that there are other heroes and before you can join the quest, we need you to sign up for... legal and tracking purposes.",
                  "Like.... not evil tech tracking just... who are you and how far are you in this quest its really no big deal....",
                  "It actually sounds much worse now that I am trying to explain it..."],
    CK.NEXT_PATH.value: ["GET to auth/register for your next instructions."]
}

@bp.route('/start', methods=['GET'])
@bp.route('/start/<username>', methods=['GET'])
def start(username=None):
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
