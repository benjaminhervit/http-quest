import pytest

from app.quest import QuestData
from app.enums import ContentKeys, QuestState
import app.utils.content_generator as cont_gen


@pytest.fixture
def quest_data():
    return QuestData(
        title="title",
        start_message="start",
        quest="quest",
        completed="completed",
        locked="locked",
        next_path="next",
        url_prefix="prefix",
        xp=1,
        hints=["hint1", "hint2"],
        failed="failed",
    )


def test_locked_content(quest_data: QuestData):
    content = cont_gen.create_locked_content(quest_data)
    keys = set(
        [
            ContentKeys.STATUS.value,
            ContentKeys.TITLE.value,
            ContentKeys.STORY.value,
            ContentKeys.QUEST.value,
            ContentKeys.NEXT_PATH.value,
            ContentKeys.HINTS.value,
        ]
    )

    assert set(content) == keys
    assert content.get(ContentKeys.STATUS.value) == QuestState.LOCKED.value
    assert content.get(ContentKeys.STATUS.value) == "locked"
    assert content.get(ContentKeys.TITLE.value) == "title"
    assert content.get(ContentKeys.STORY.value) == quest_data.locked
    assert content.get(ContentKeys.STORY.value) == "locked"
    assert not content.get(ContentKeys.QUEST.value)
    assert content.get(ContentKeys.QUEST.value) == ""
    assert content.get(ContentKeys.NEXT_PATH.value) == ""
    assert not content.get(ContentKeys.NEXT_PATH.value)
    assert content.get(ContentKeys.HINTS.value) == "No hints just yet"


def test_start_content(quest_data: QuestData):
    content = cont_gen.create_start_content(quest_data)
    keys = set(
        [
            ContentKeys.STATUS.value,
            ContentKeys.TITLE.value,
            ContentKeys.STORY.value,
            ContentKeys.QUEST.value,
            ContentKeys.NEXT_PATH.value,
            ContentKeys.HINTS.value,
        ]
    )

    assert set(content) == keys
    assert content.get(ContentKeys.STATUS.value) == QuestState.UNLOCKED.value
    assert content.get(ContentKeys.STATUS.value) == "unlocked"
    assert content.get(ContentKeys.TITLE.value) == "title"
    assert content.get(ContentKeys.STORY.value) == quest_data.start_message
    assert content.get(ContentKeys.STORY.value) == "start"
    assert content.get(ContentKeys.QUEST.value) == quest_data.quest
    assert content.get(ContentKeys.QUEST.value) == "quest"
    assert content.get(ContentKeys.NEXT_PATH.value) == ""
    assert not content.get(ContentKeys.NEXT_PATH.value)
    assert content.get(ContentKeys.HINTS.value) == quest_data.hints
    assert content.get(ContentKeys.HINTS.value) == ["hint1", "hint2"]


def test_completed_content(quest_data: QuestData):
    content = cont_gen.create_completed_content(quest_data)
    keys = set(
        [
            ContentKeys.STATUS.value,
            ContentKeys.TITLE.value,
            ContentKeys.STORY.value,
            ContentKeys.QUEST.value,
            ContentKeys.NEXT_PATH.value,
            ContentKeys.HINTS.value,
        ]
    )

    assert set(content) == keys
    assert content.get(ContentKeys.STATUS.value) == QuestState.COMPLETED.value
    assert content.get(ContentKeys.STATUS.value) == "completed"
    assert content.get(ContentKeys.TITLE.value) == "title"
    assert content.get(ContentKeys.STORY.value) == quest_data.completed
    assert content.get(ContentKeys.STORY.value) == "completed"
    assert content.get(ContentKeys.QUEST.value) == quest_data.quest
    assert content.get(ContentKeys.QUEST.value) == "quest"
    assert content.get(ContentKeys.NEXT_PATH.value) == "next"
    assert content.get(ContentKeys.HINTS.value) == quest_data.hints
    assert content.get(ContentKeys.HINTS.value) == ["hint1", "hint2"]


def test_failed_content(quest_data: QuestData):
    content = cont_gen.create_failed_content(quest_data)
    keys = set(
        [
            ContentKeys.STATUS.value,
            ContentKeys.TITLE.value,
            ContentKeys.STORY.value,
            ContentKeys.QUEST.value,
            ContentKeys.NEXT_PATH.value,
            ContentKeys.HINTS.value,
        ]
    )

    assert set(content) == keys
    assert content.get(ContentKeys.STATUS.value) == QuestState.FAILED.value
    assert content.get(ContentKeys.STATUS.value) == "failed"
    assert content.get(ContentKeys.TITLE.value) == "title"
    assert content.get(ContentKeys.STORY.value) == quest_data.failed
    assert content.get(ContentKeys.STORY.value) == "failed"
    assert content.get(ContentKeys.QUEST.value) == quest_data.quest
    assert content.get(ContentKeys.QUEST.value) == "quest"
    assert content.get(ContentKeys.NEXT_PATH.value) == ""
    assert content.get(ContentKeys.HINTS.value) == quest_data.hints
    assert content.get(ContentKeys.HINTS.value) == ["hint1", "hint2"]


@pytest.mark.parametrize(
    "state, values",
    [
        # query test
        (
            QuestState.LOCKED.value,
            [QuestState.LOCKED.value, "title", "locked", "", "", "No hints just yet"],
        ),
        (
            QuestState.UNLOCKED.value,
            [
                QuestState.UNLOCKED.value,
                "title",
                "start",
                "quest",
                "",
                ["hint1", "hint2"],
            ],
        ),
        (
            QuestState.COMPLETED.value,
            [
                QuestState.COMPLETED.value,
                "title",
                "completed",
                "quest",
                "next",
                ["hint1", "hint2"],
            ],
        ),
        (
            QuestState.FAILED.value,
            [
                QuestState.FAILED.value,
                "title",
                "failed",
                "quest",
                "",
                ["hint1", "hint2"],
            ],
        ),
    ],
)
def test_content_creator(quest_data: QuestData, state, values):
    content = cont_gen.create_content(quest_data, state)
    keys = set(
        [
            ContentKeys.STATUS.value,
            ContentKeys.TITLE.value,
            ContentKeys.STORY.value,
            ContentKeys.QUEST.value,
            ContentKeys.NEXT_PATH.value,
            ContentKeys.HINTS.value,
        ]
    )

    assert set(content) == keys
    assert content.get(ContentKeys.STATUS.value) == values[0]
    assert content.get(ContentKeys.STATUS.value) == state
    assert content.get(ContentKeys.TITLE.value) == values[1]
    assert content.get(ContentKeys.STORY.value) == values[2]
    assert content.get(ContentKeys.QUEST.value) == values[3]
    assert content.get(ContentKeys.NEXT_PATH.value) == values[4]
    assert content.get(ContentKeys.HINTS.value) == values[5]
