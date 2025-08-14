from flask import Request
from app.utils import content_generator
from app.quest import QuestData

def get_handlers_map():
    return {
        'GET': get_handler
    }

def get_handler(quest: QuestData, req: Request):
    content = content_generator.create_locked_content(quest)
    username = req.view_args.get('username') if req.view_args else None
    
    if username:
        content = content_generator.create_completed_content(quest)
        placeholder_map = {'[HERO]': username}
        content = content_generator.replace_placeholders(content,
                                                         placeholder_map)
    else:
        content = content_generator.create_start_content(quest)
    return content