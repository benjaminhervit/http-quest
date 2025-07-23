from app.enums import QuestState

def set_locked(this_state: QuestState) -> QuestState:
    return QuestState.LOCKED

def set_closed(this_state: QuestState) -> QuestState:
    return QuestState.CLOSED

def set_by_active_state(this_state: QuestState) -> QuestState:
    # will update with most appropriate state based on the stated given
    if this_state == QuestState.FAILED:
        return QuestState.UNLOCKED
    if this_state == QuestState.COMPLETED:
        return QuestState.CLOSED
    return this_state
