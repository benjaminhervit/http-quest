from app.enums import QuestState

def build_json_string(data: list[str] | str) -> str:
    if isinstance(data, str):
        return data
    if data and all(isinstance(i, str) for i in data):
        return "\n".join(data)
    return ""

def create_locked_response(quest: dict) -> dict:
    #Assumes bad request and quest is locked as a start
    return {
             'status': QuestState.LOCKED.value,
             'title': build_json_string(quest['title']),
             'story': "This path is still locked for you.",
             'quest': "",
             'next_path': ""
             }


def create_start_response(quest: dict) -> dict:
    resp = create_locked_response(quest)
    resp.update({'status': QuestState.UNLOCKED.value})
    resp.update({'story': build_json_string(quest['start_message'])})
    resp.update({'quest': build_json_string(quest['quest'])})
    return resp


def create_completed_response(quest: dict) -> dict:
    resp = create_start_response(quest)
    resp.update({'status': QuestState.COMPLETED.value})
    resp.update({'story': build_json_string(quest['completed'])})
    resp.update({'next_path': build_json_string(quest['next_path'])})
    return resp