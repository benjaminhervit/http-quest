from flask import request, render_template, session
import json
from app.blueprints.quest_render import bp


@bp.route('/', methods=['GET'])
def renderer():
    content = session.pop('content', None)
    print(content)
    return render_template('quest_renderer.html', content=content)
