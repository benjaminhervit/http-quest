from flask import Request
from app.utils import content_generator
from app.quest import QuestData
from app.enums import QuestState


def get_handlers():
    return {"GET": get_handler}


def get_handler(quest: QuestData, req: Request):
    state = QuestState.LOCKED.value
    content = content_generator.create_locked_content(quest)
    formatting = {"[HERO]": "[HERO]"}
    username = req.view_args.get("username") if req.view_args else None
    if username:
        formatting.update({"HERO": username})
        state = QuestState.COMPLETED.value
        #content = content_generator.create_completed_content(quest)
    else:
        state = QuestState.UNLOCKED.value
        #content = content_generator.create_start_content(quest)
    #content = content_generator.format_content(content, formatting)
    content = content_generator.create_content(quest, state, formatting)
    return content
