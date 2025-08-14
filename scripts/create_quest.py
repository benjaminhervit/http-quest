import os
import sys
from slugify import slugify

BASE_PATH = "app/blueprints/quests"

TEMPLATE_DATA = '''
from app.quest import QuestData
    def get_quest():
        return QuestData(
            title="{title}",
            start_message="",
            quest="",
            completed="",
            locked="",
            next_path="",
            hint="",
            url_prefix="/game"
        )
'''

TEMPLATE_HANDLER_FILE = '''
from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils, standard_get_handler
from app.authentication_manager import authenticator

def get_handlers():
    return {
        'GET': get_handler,
        'POST': post_handler
    }


def get_handler(quest: QuestData, req: Request):
    return standard_get_handler(req=req, quest=quest)


def post_handler(quest: QuestData, req: Request):
    #username = parser_utils.get_auth_username(req)
    #if authenticator.authenticate(req):
    #    pass
    return "get_handler template"
'''

ROUTE_TEMPLATE_FILE = '''
from flask import request

from .data import get_quest
from .handlers import get_handlers

from app.blueprints.quests import bp
from app.request_manager import RequestHandler

@bp.route("/", methods=['GET'])
def {slug}_route():
    handlers = get_handlers()
    quest = get_quest()
    valid_methods = ['GET']
    response = RequestHandler.execute(request, quest, handlers, valid_methods)
    return response
'''

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