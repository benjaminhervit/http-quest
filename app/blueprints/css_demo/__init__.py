from flask import Blueprint

bp = Blueprint("css", __name__, url_prefix="/css")

from . import routes
