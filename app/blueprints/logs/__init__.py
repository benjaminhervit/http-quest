from flask import Blueprint

bp = Blueprint("log", __name__, url_prefix="/log")

from . import routes
