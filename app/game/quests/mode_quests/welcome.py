from app.models.quest import Quest
from app.game.quests.mode_quests.accept import accept_Q

welcome_Q = Quest(
    title="Welcome",
    story="Welcome to a CRUDe game! The (re)quest to claim the CRUDe crown!",
    directions="you should get here when registering?",
    quest="To get started, simply follow the directions.",

    success_response="We have lucky to have you here.",
    failed_response="... You should not even be able to fail this... How???",
    is_locked_response="How did you even get here? This quest is LOCKED! Go back where you came from!",
    is_completed_response="What are you even doing here?? Get goin!",
    solution_fn="NONE",
    
    req_method="GET",
    username_loc="PATH",
    token_loc="NONE",
    answer_loc="NONE",
    answer_key="NONE",
    auth_type="USERNAME",
    )

welcome_Q.next_quest=accept_Q