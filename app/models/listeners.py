from sqlalchemy import event, inspect
from sqlalchemy.orm import Session
from flask import has_app_context
from typing import cast

from app.models.user import User
from app.models.quest import Quest
from app.models.user_quest_state import UserQuestState
from app.enums import QuestState
from app.extensions import db

FIRST_TITLE = 'welcome'

@event.listens_for(db.session, "after_flush")
def populate_user_state_after_commit(session, flush_context):
    if not has_app_context():
        print("NO CONTEXT FOR POPULATE QUEST LISTENER!")
        return

    for obj in session.new:
        if isinstance(obj, User):
            quests: list[Quest] = Quest.query.all()
            for quest in quests:
                is_first = quest.slug == FIRST_TITLE
                
                state = (QuestState.UNLOCKED.value if is_first
                         else QuestState.LOCKED.value)
                
                uqs: UserQuestState = UserQuestState(
                    username=obj.username,
                    slug=quest.slug,
                    state=state
                )
                db.session.add(uqs)
                


# @event.listens_for(Session, 'after_flush_postexec')
# def unlock_next_quests_on_closed(session, flush_context):
#     """
#     Detects changes to quest states and unlocks new quests if the quest has been closed.
#     """
#     print(f"HERE: {session.dirty}")
#     for obj in session.dirty:
#         print("HERE2")
#         if isinstance(obj, UserQuestState):
#             state: UserQuestState = inspect(obj)
#             if state.attrs.state.history.has_changes():
#                 new_value = state.attrs.state.history.added[0] if state.attrs.state.history.added else None
#                 if new_value[0] == QuestState.CLOSED.value:
#                     username: str = target.username
#                     slug: str = target.slug
#                     method: str = target.method
                    
#                     this_quest: Quest | None = Quest.get_by_slug_and_method(slug, method)
#                     if this_quest:
#                         print(f"NEXT: {this_quest.next_quests}")
#                         for q in this_quest.next_quests:
#                             print(q.to_dict())
#                             uqs = UserQuestState.get_uqs(username, slug, method)
#                             if uqs and uqs.state == QuestState.LOCKED.value:
#                                 UserQuestState.update_state(QuestState.UNLOCKED.value, uqs)