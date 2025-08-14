from flask import jsonify, render_template, Request
from app.utils import browser_detector
from app import services


def send_response(
    req: Request, content: dict, status_code: int, html: str = "quest_renderer.html"
):

    if browser_detector.is_browser_request(req):
        headers, table = services.get_progress_matrix()
        return (
            render_template(html, content=content, headers=headers, table=table),
            status_code,
        )
    return jsonify({"content": content}), status_code
