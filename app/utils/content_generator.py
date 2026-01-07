from typing import Any
import re
import textwrap
import random

from app.enums import QuestState, ContentKeys, StatusCode
from app.quest import QuestData


def create_content(
    quest: QuestData, quest_state: str, formatting: dict | None = None
) -> dict:

    formatting = formatting or get_base_formatting()

    content_map: dict = {
        QuestState.LOCKED.value: create_locked_content(quest),
        QuestState.UNLOCKED.value: create_start_content(quest),
        QuestState.COMPLETED.value: create_completed_content(quest),
        QuestState.FAILED.value: create_failed_content(quest),
    }

    content: dict | None = content_map.get(quest_state, None)
    if not content:
        raise ValueError(
            (
                f"Could not create content for quest {quest.title}"
                "with state {quest_state}"
            ),
            StatusCode.SERVER_ERROR.value,
        )

    content = format_content(content, formatting)
    return content
    

def create_error_msg(msg: str, error_type: str, status_code: int) -> dict:
    return {
        ContentKeys.ERROR_MSG.value: msg,
        ContentKeys.ERROR_TYPE.value: error_type,
        ContentKeys.STATUS_CODE.value: status_code,
    }


def create_locked_content(quest: QuestData) -> dict:
    return {
        ContentKeys.STATUS.value: QuestState.LOCKED.value,
        ContentKeys.TITLE.value: quest.title,
        ContentKeys.STORY.value: quest.locked,
        ContentKeys.QUEST.value: "",
        ContentKeys.NEXT_PATH.value: "",
        ContentKeys.HINTS.value: "No hints just yet",
    }


def clean_text(s: str) -> str:
    # remove common leading indentation and trim ends
    s = textwrap.dedent(s).strip()
    # collapse multiple spaces/tabs inside each line
    s = "\n".join(re.sub(r"[ \t]+", " ", line).rstrip() for line in s.splitlines())
    return s


def format_string(string: str, formatting: dict):
    if not formatting:
        raise ValueError(f"formatting cannot by falsy: {formatting}")

    try:
        formatted = string.format(**formatting).replace("\n", "")
        formatted = clean_text(formatted)
        return formatted
    except KeyError:
        raise KeyError(f"Missing key in formatter {formatting}")


def format_content(content: dict[str, Any], formatting: dict[str, str]):
    for k, v in content.items():
        if isinstance(v, str):
            content[k] = format_string(v, formatting)
        elif isinstance(v, list):
            formatted = []
            for i in v:
                t = format_string(i, formatting)
                formatted.append(t)
            content[k] = formatted
    return content


def get_base_formatting():
    attributes = [
        "enigmatic",
        "shadow-veiled",
        "whisper-walking",
        "myth-wrapped",
        "legend-breathing",
        "phantom-hearted",
        "star-touched",
        "riddle-minded",
        "moonlit",
        "mirage-born",
        "secret-keeper",
        "arcane-gifted",
        "fortune-favored",
        "destiny-dancing",
        "paradoxical",
        "unsong",
    ]
    three_attributes = ", ".join(random.sample(attributes, 3))
    return {"HERO": "unknown, " + three_attributes + " hero"}


def create_start_content(quest: QuestData) -> dict:
    content = create_locked_content(quest)  # get base

    content.update({ContentKeys.STATUS.value: QuestState.UNLOCKED.value})
    content.update({ContentKeys.STORY.value: quest.start_message})
    content.update({ContentKeys.QUEST.value: quest.quest})
    content.update({ContentKeys.HINTS.value: quest.hints})
    return content


def create_completed_content(quest: QuestData) -> dict:
    content = create_start_content(quest)  # get base

    content.update({ContentKeys.STATUS.value: QuestState.COMPLETED.value})
    content.update({ContentKeys.STORY.value: quest.completed})
    content.update({ContentKeys.NEXT_PATH.value: quest.next_path})
    content.update({ContentKeys.LEARNING.value: quest.learning})
    return content


def create_failed_content(quest: QuestData) -> dict:
    content = create_start_content(quest)  # get base

    content.update({ContentKeys.STATUS.value: QuestState.FAILED.value})
    content.update({ContentKeys.STORY.value: quest.failed})
    return content
