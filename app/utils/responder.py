from flask import jsonify, render_template, Request
from app.utils import parser_utils
from app import services


def send_response(req: Request, content: dict, 
                  status_code: int, html: str = "quest_renderer.html"):

    if parser_utils.request_accepts_html(req):
        data = services.get_leaderboard()
        return (
            render_template(html, content=content, data=data),
            status_code,)
    return jsonify({"content": content}), status_code
