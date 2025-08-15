from sqlalchemy import event, insert, select, update, literal, case, func, inspect
from app.models import User, Quest, UserQuestState
from app.enums import QuestState

print("event listeners registered")

@event.listens_for(Quest, "after_insert")
def backfill_states_for_new_quest(mapper, connection, target: Quest):
    user_tbl = User.__table__
    uqs_tbl = UserQuestState.__table__

    insert_statement = insert(uqs_tbl).from_select(
        ["username", "quest", "state"],
        select(
            user_tbl.c.username,
            literal(target.title),
            literal(QuestState.UNLOCKED.value),  # or UNLOCKED if you prefer
        ),
    )
    connection.execute(insert_statement)


@event.listens_for(User, "after_insert")
def create_user_quest_states(mapper, connection, target: User):
    quest_tbl = Quest.__table__
    uqs_tbl = UserQuestState.__table__

    completed_titles = ("Welcome", "Registration")

    state_expr = case(
        (quest_tbl.c.title.in_(completed_titles), literal(QuestState.COMPLETED.value)),
        else_=literal(QuestState.UNLOCKED.value),
    )

    stmt = insert(uqs_tbl).from_select(
        ["username", "quest", "state"],
        select(literal(target.username), quest_tbl.c.title, state_expr),
    )
    connection.execute(stmt)
