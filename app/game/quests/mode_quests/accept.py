from app.models.quest import Quest
from app.game.quests.mode_quests.null_q import null_Q

accept_Q = Quest(
    title="Welcome",
    story="You stand in front of a big decision... ish...",
    directions="POST yes after your name in the PATH to accept this epic reQUEST.",
    quest="To get started, simply follow the directions.",

    success_response="HORAY! WONDERFUL!",
    failed_response="That is not how you accept a quest! Try again!",
    is_locked_response="That is not how you accept a quest! Try again!",
    is_completed_response="You have already accepted the quest. GET GOING!",
    solution="yes",
    solution_fn="SINGLE_INPUT",
    
    req_method="POST",
    username_loc="PATH",
    token_loc="NONE",
    answer_loc="QUERY",
    answer_key="answer",
    auth_type="USERNAME",
    )

accept_Q.next_quest = null_Q