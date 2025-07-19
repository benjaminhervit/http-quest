from app.models.quest import Quest

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


# accept_q = QuestData(
#     #TXT
#     title="Welcome",
#     story_txt="You stand in front of a big decision... ish...",
#     directions_txt = "POST yes after your name in the PATH to accept this epic reQUEST.",
#     quest_txt="To get started, simply follow the directions.",
#     response_wrong_txt="That is not how you accept a quest! Try again!",
#     response_correct_txt="HORAY! WONDERFUL!",
#     response_completed_txt="You have already accepted the quest. GET GOING!",
    
#     #functions
#     correct_answer="yes",
#     quest_validator_type="SINGLE_INPUT",
    
#     #next
#     next_quest_directions = empty_quest.directions_txt,
    
#     request_settings = RequestSettings(
#         req_method='POST',
#         answer_location='QUERY',
#         answer_key='answer',
#         auth_type='USERNAME',
#         token_location='NONE',
#         username_location='PATH'
#     )
# )