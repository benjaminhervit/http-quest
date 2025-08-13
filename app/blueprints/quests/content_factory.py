from app.enums import QuestState, ContentKeys
from app.quest import QuestData


def create_error_msg(msg: str, error_type: str, status_code: int) -> dict:
    return {
        ContentKeys.ERROR_MSG.value: msg,
        ContentKeys.ERROR_TYPE.value: error_type,
        ContentKeys.STATUS_CODE.value: status_code
    }


def replace_placeholders(content: dict, placeholder_map: dict):
    updated_content = dict()
    if isinstance(content, dict) and isinstance(placeholder_map, dict):
        for placeholder, real_value in placeholder_map.items():
            for key, value in content.items():
                updated_content[key] = value.replace(placeholder, real_value) 
    return updated_content


def build_json_string(data: list[str] | str) -> str:
    if isinstance(data, str):
        return data
    if data and all(isinstance(i, str) for i in data):
        return "\n".join(data)
    return ""


def create_locked_content(quest: QuestData) -> dict:
    #Assumes bad request and quest is locked as a start
    return {
             ContentKeys.STATUS.value: QuestState.LOCKED.value,
             ContentKeys.TITLE.value: build_json_string(
                 quest.title),
             ContentKeys.STORY.value: quest.locked,
             ContentKeys.QUEST.value: "",
             ContentKeys.NEXT_PATH.value: ""
             }

def create_start_content(quest: QuestData) -> dict:
    content = create_locked_content(quest)
    content.update({ContentKeys.STATUS.value: QuestState.UNLOCKED.value})
    content.update({ContentKeys.STORY.value: build_json_string(quest.start_message)})
    content.update({ContentKeys.QUEST.value: build_json_string(quest.quest)})
    return content


def create_completed_content(quest: QuestData, 
                             placeholder_map: dict | None = None) -> dict:
    #  build content
    content = create_start_content(quest)
    content.update({ContentKeys.STATUS.value: QuestState.COMPLETED.value})
    content.update({ContentKeys.STORY.value: build_json_string(quest.completed)})
    content.update({ContentKeys.NEXT_PATH.value: build_json_string(quest.next_path)})
    return content
