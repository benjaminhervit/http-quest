from sqlalchemy import event, inspect
from sqlalchemy.orm import Session
from flask import has_app_context
from typing import cast

from app.models.user import User
from app.models.quest import Quest
from app.models.user_quest_state import UserQuestState
from app.enums import QuestState
from app.extensions import db

@event.listens_for(db.session, "after_flush")
def populate_user_state_after_commit(session, flush_context):
    if not has_app_context():
        print("NO CONTEXT FOR POPULATE QUEST LISTENER!")
        return

    for obj in session.new:
        if isinstance(obj, User):
            quests: list[Quest] = Quest.query.all()
            for quest in quests:
                if not quest.is_stateless:    
                    uqs: UserQuestState = UserQuestState(
                        username=obj.username,
                        slug=quest.slug,
                        state=state
                    )
                    db.session.add(uqs)
                    
@event.listens_for(Quest, 'before_insert')
def validate_quest_before_insert(mapper, connection, target: Quest):
    print(f'Validating {target.title} from before_insert')
    target.validate()

@event.listens_for(Quest, 'before_update')
def validate_quest_before_update(mapper, connection, target: Quest):
    print(f'Validating {target.title} from before_update')
    target.validate()