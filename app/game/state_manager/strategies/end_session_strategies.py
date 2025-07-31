from app.enums import QuestState

def set_completed(this_state: QuestState) -> QuestState:
    if not isinstance(this_state, QuestState):
        raise ValueError(f"Could not create end state from {this_state}")
    return QuestState.COMPLETED

def set_by_active_state(this_state: QuestState) -> QuestState:
    # will update with most appropriate state based on the stated given
    if not isinstance(this_state, QuestState):
        raise ValueError(f"Could not create end state from {this_state}")

    if this_state == QuestState.FAILED:
        return QuestState.UNLOCKED
    if this_state == QuestState.COMPLETED:
        return QuestState.CLOSED
    return this_state
