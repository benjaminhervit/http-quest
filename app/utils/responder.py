from flask import jsonify, render_template

def respond(content: dict, status_code: int, return_html: bool = False,
            html: str = 'quest_renderer.html'):
    
    if return_html:
        return render_template(html, content=content)
    return jsonify({
        'content': content
    }, status_code)
