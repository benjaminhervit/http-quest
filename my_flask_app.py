"""
This module contains a simple Flask application with route handling.
"""

import json
# from game.level import Level, LevelEnum as L
from game import level_builder
# from game.routes import Route as R
# from game.status_code import StatusCode
from game.level import Level, LevelEnum as L
# import game.response_builder as RB
from game.routes import Route as R
# from quest_db import QuestDB

import game.response_builder as RB

from quest_db import QuestDB

from flask import Flask

app = Flask(__name__)

routes_functions = {
    '/':lambda:"Hello world",
    '/hi':lambda: "Hi"}

@app.route('/path:<route>')
def routes_handler(route):
    """"""
    print(route)
    if route in routes_functions:
        return routes_functions.get(route)()
    return "Route not found", 404
    
if __name__ == "__main__":
    app.run(debug=True)
