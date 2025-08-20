#!/usr/bin/env python3

#to make executable: chmod +x scripts/create_quest.py 
import os
import sys
from slugify import slugify

BASE_PATH = "app/blueprints/quests"

TEMPLATE_DATA = """
from app.quest import QuestData
    def get_quest():
        return QuestData(
            title="{title}",
            start_message="",
            quest="",
            completed="",
            locked="",
            next_path="",
            xp=1,
            hints=[],
            url_prefix="/game"
        )
"""

TEMPLATE_HANDLER_FILE = """
from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.authentication_manager import authenticator
from app.enums import QuestState


def get_handlers():
    return {
        'GET': get_handler,
        'POST': post_handler
    }


def get_handler(quest: QuestData, req: Request):
    state = QuestState.LOCKED.value
    formatting = content_generator.get_base_formatting()
    return "get handler template"


def post_handler(quest: QuestData, req: Request):
    state = QuestState.LOCKED.value
    formatting = content_generator.get_base_formatting()
    return "post_handler template"
"""

ROUTE_TEMPLATE_FILE = """
from flask import request

from .data import get_quest
from .handlers import get_handlers

from app.blueprints.quests import bp
from app.request_manager import QuestRequestHandler
from app.authentication_manager import authenticate_with_username

@bp.route("/", methods=['GET'])
def {slug}_route():
    handlers = get_handlers()
    quest = get_quest()
    valid_methods = ['GET']
    response = QuestRequestHandler.execute(
        req=request,
        quest=quest,
        authenticator=authenticate_with_username,
        handlers_map=handlers,
        valid_req_methods=valid_methods)
    return response
"""


def create_quest(name):
    slug = slugify(name)
    folder_name = f"{slug}_quest"
    path = os.path.join(BASE_PATH, folder_name)

    if os.path.exists(path):
        print(f"ERROR! Path already exists: {path}")
        return

    os.makedirs(path)

    with open(os.path.join(path, "data.py"), "w") as f:
        f.write(TEMPLATE_DATA.format(title=name))

    with open(os.path.join(path, "handlers.py"), "w") as f:
        f.write(TEMPLATE_HANDLER_FILE)

    with open(os.path.join(path, "routes.py"), "w") as f:
        f.write(ROUTE_TEMPLATE_FILE.format(slug=slug))

    open(os.path.join(path, "__init__.py"), "w").close()
    print("Quest template created successfully")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "--name":
        print("Usage: python create_quest.py --name 'name_of_quest'")
        sys.exit(1)

    create_quest(sys.argv[2])
