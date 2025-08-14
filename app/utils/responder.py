from flask import jsonify, render_template, Request
from app.utils import browser_detector

def send_response(req: Request, content: dict, status_code: int,
                  html: str = 'quest_renderer.html'):
    
    if browser_detector.is_browser_request(req):
        return render_template(html, content=content)
    return jsonify({
        'content': content
    }), status_code
