from flask import Flask, render_template, redirect, url_for, request, g, abort, jsonify, Response, send_file, make_response
import mimetypes
import json
from urllib.parse import unquote, quote

from game.level import Level, LevelEnum as L
import game.level_builder as level_builder
from game.routes import Route as R
from game.status_code import StatusCode

import game.response_builder as RB

from quest_db import QuestDB

app = Flask(__name__)

routes_functions = {
    '/':lambda:"Hello world",
    '/hi':lambda: "Hi",
    '/world':lambda: "world",
}

@app.route('/path:<route>')
def routes_handler(route):
    """"""
    print(route)
    if route in routes_functions:
        return routes_functions.get(route)()
    return "Route not found", 404
    
if __name__ == "__main__":
    app.run(debug=True)
