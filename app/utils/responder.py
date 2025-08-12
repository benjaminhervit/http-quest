from flask import jsonify, render_template

def respond(content: dict, status_code: int, return_html: bool = False):
    if return_html:
        return render_template('quest_renderer.html', content=content)
    return jsonify({
        'content': content
    }, status_code)
