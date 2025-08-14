from flask import Request
from app.utils import content_generator
from app.quest import QuestData


def get_handlers():
    return {"GET": get_handler}


def get_handler(quest: QuestData, req: Request):
    content = content_generator.create_locked_content(quest)
    username = req.view_args.get("username") if req.view_args else None

    if username:
        formatting = {"HERO": username}
        content = content_generator.create_completed_content(quest, formatting)
    else:
        content = content_generator.create_start_content(quest)
    return content
