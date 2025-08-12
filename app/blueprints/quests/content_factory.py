from app.enums import QuestState, ContentKeys


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


def create_locked_content(quest: dict) -> dict:
    #Assumes bad request and quest is locked as a start
    return {
             ContentKeys.STATUS.value: QuestState.LOCKED.value,
             ContentKeys.TITLE.value: build_json_string(
                 quest[ContentKeys.TITLE.value]),
             ContentKeys.STORY.value: "This path is still locked for you.",
             ContentKeys.QUEST.value: "",
             ContentKeys.NEXT_PATH.value: ""
             }

def create_start_content(quest: dict) -> dict:
    content = create_locked_content(quest)
    content.update({ContentKeys.STATUS.value: QuestState.UNLOCKED.value})
    content.update({ContentKeys.STORY.value: build_json_string(
        quest[ContentKeys.START_MESSAGE.value])})
    content.update({ContentKeys.QUEST.value: build_json_string(
        quest[ContentKeys.QUEST.value])})
    return content


def create_completed_content(quest: dict, 
                             placeholder_map: dict | None = None) -> dict:
    #  build content
    content = create_start_content(quest)
    content.update({ContentKeys.STATUS.value: QuestState.COMPLETED.value})
    content.update({ContentKeys.STORY.value: build_json_string(
        quest[ContentKeys.COMPLETED.value])})
    content.update({ContentKeys.NEXT_PATH.value: build_json_string(
        quest[ContentKeys.NEXT_PATH.value])})

    return content
