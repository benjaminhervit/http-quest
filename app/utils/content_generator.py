from app.enums import QuestState, ContentKeys
from app.quest import QuestData


def create_content(quest: QuestData, quest_state: str, formatting: dict) -> dict | None:
    content_map: dict = {
        QuestState.LOCKED.value: create_locked_content(quest, formatting),
        QuestState.UNLOCKED.value: create_start_content(quest, formatting),
        QuestState.COMPLETED.value: create_completed_content(quest, formatting),
        QuestState.FAILED.value: create_completed_content(quest, formatting),
    }
    
    return content_map.get(quest_state)


def create_error_msg(msg: str, error_type: str, status_code: int) -> dict:
    return {
        ContentKeys.ERROR_MSG.value: msg,
        ContentKeys.ERROR_TYPE.value: error_type,
        ContentKeys.STATUS_CODE.value: status_code
    }


def create_locked_content(quest: QuestData, formatting: dict | None = None) -> dict:
    #Assumes bad request and quest is locked as a start
    formatting = formatting or {}
    title: str = format_string(quest.title, formatting)
    story: str = format_string(quest.locked, formatting)
    
    return {
             ContentKeys.STATUS.value: QuestState.LOCKED.value,
             ContentKeys.TITLE.value: title,
             ContentKeys.STORY.value: story,
             ContentKeys.QUEST.value: "",
             ContentKeys.NEXT_PATH.value: "",
             ContentKeys.HINT.value: "No hints just yet"
             }


def format_string(string: str, fomatting: dict):
    formatted = string.format(**fomatting).replace("\n", "")
    return formatted


def create_start_content(quest: QuestData, formatting: dict | None = None) -> dict:
    formatting = formatting or {}
    content = create_locked_content(quest, formatting)
    
    status = QuestState.UNLOCKED.value
    story = format_string(quest.start_message, formatting)
    quest_txt = format_string(quest.quest, formatting)
    hint = format_string(quest.hint, formatting)
    
    content.update({ContentKeys.STATUS.value: status})
    content.update({ContentKeys.STORY.value: story})
    content.update({ContentKeys.QUEST.value: quest_txt})
    content.update({ContentKeys.HINT.value: hint})
    return content


def create_completed_content(quest: QuestData, formatting: dict | None = None) -> dict:
    formatting = formatting or {}
    content = create_start_content(quest, formatting)
    
    status = QuestState.COMPLETED.value
    story = format_string(quest.completed, formatting)
    next_path = format_string(quest.next_path, formatting)
    
    content.update({ContentKeys.STATUS.value: status})
    content.update({ContentKeys.STORY.value: story})
    content.update({ContentKeys.NEXT_PATH.value: next_path})
    return content


def create_failed_content(quest: QuestData, formatting: dict | None = None) -> dict:
    formatting = formatting or {}
    content = create_start_content(quest, formatting)
    
    status = QuestState.COMPLETED.value
    story = format_string(quest.failed, formatting)
    next_path = format_string(quest.next_path, formatting)
    
    content.update({ContentKeys.STATUS.value: status})
    content.update({ContentKeys.STORY.value: story})
    content.update({ContentKeys.NEXT_PATH.value: next_path})
    return content
