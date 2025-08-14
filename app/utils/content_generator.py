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


def create_locked_content(quest: QuestData, format_map: dict = {}) -> dict:
    #Assumes bad request and quest is locked as a start
    return {
             ContentKeys.STATUS.value: QuestState.LOCKED.value,
             ContentKeys.TITLE.value: quest.title.format(**format_map),
             ContentKeys.STORY.value: quest.locked.format(**format_map),
             ContentKeys.QUEST.value: "",
             ContentKeys.NEXT_PATH.value: "",
             ContentKeys.HINT.value: "No hints just yet"
             }

def create_start_content(quest: QuestData, format_map: dict = {}) -> dict:
    content = create_locked_content(quest, format_map)
    content.update({ContentKeys.STATUS.value: QuestState.UNLOCKED.value})
    content.update({ContentKeys.STORY.value: quest.start_message.format(**format_map)})
    content.update({ContentKeys.QUEST.value: quest.quest.format(**format_map)})
    content.update({ContentKeys.HINT.value: quest.hint.format(**format_map)})
    return content


def create_completed_content(quest: QuestData, format_map: dict = {}) -> dict:
    content = create_start_content(quest, format_map)
    content.update({ContentKeys.STATUS.value: QuestState.COMPLETED.value})
    content.update({ContentKeys.STORY.value: quest.completed.format(**format_map)})
    content.update({ContentKeys.NEXT_PATH.value: quest.next_path.format(**format_map),})
    return content
