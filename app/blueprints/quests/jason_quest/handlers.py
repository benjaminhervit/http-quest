from flask import Request

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.enums import QuestState

def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_handler(quest: QuestData, req: Request):
    state = QuestState.UNLOCKED.value
    username = parser_utils.get_auth_username(req) or "HERO"
    formatting = {"HERO": username}
    content = content_generator.create_content(quest, state, formatting)
    return content


def post_handler(quest: QuestData, req: Request):
    state = QuestState.LOCKED.value
    formatting = content_generator.get_base_formatting()
    
    print(f"JSON: {parser_utils.get_json(req)}")
    
    hire_jason = parser_utils.get_field_from_request_data(
        req, "jason", parser_utils.get_json
    )
    
    state = QuestState.FAILED.value  # if parsing succeeds - assume failure
    if hire_jason == "hired":
        print("WOHO!")
        state = QuestState.COMPLETED.value  # if parsing succeeds - assume failure
        username = parser_utils.get_auth_username(req)
        if username:
            formatting.update({"HERO": username})

    content = content_generator.create_content(quest, state, formatting)
    
    return content
