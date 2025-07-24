from app.enums import QuestState

def set_completed(this_state: QuestState) -> QuestState:
    return QuestState.COMPLETED

def set_by_active_state(this_state: QuestState) -> QuestState:
    # will update with most appropriate state based on the stated given
    if this_state == QuestState.FAILED:
        return QuestState.UNLOCKED
    if this_state == QuestState.COMPLETED:
        return QuestState.CLOSED
    return this_state
