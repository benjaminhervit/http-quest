from app.models.quest import Quest

welcome_Q = Quest(
    title="",
    story="",
    directions="There is nothing from here. This is an empty path.",
    quest="",

    success_response="",
    failed_response="",
    is_locked_response="",
    is_completed_response="",
    solution_fn="NONE",
    
    req_method="GET",
    username_loc="PATH",
    token_loc="NONE",
    answer_loc="NONE",
    answer_key="NONE",
    auth_type="USERNAME",
    )
