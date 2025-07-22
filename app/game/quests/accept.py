from app.models.quest import Quest

accept_Q = Quest(
    title="Accept",
    story="Before we begin, you must accept this reQUEST!",
    directions="GET to game/accept",
    quest="To accept you must POST a YES that I can QUERY to PATH we are standing on.",

    success_response="HORAY! WONDERFUL!",
    failed_response="That is not how you accept a quest! Try again!",
    is_locked_response="That is not how you accept a quest! Try again!",
    is_completed_response="You have already accepted the quest. GET GOING!",
    
    # solution
    expected_solution="yes",
    solution_fn="SINGLE_INPUT",
    
    # settings
    allowed_req_methods='GET,POST',
    query_keys='accept',
    input_loc="QUERY_DATA",
    )