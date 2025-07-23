from app.models.quest import Quest
from app.enums import ParserKey, AuthType

accept_Q = Quest(
    # content
    title="Accept",
    story="Before we begin, you must accept this reQUEST!",
    directions="GET to game/accept",
    quest_description="To accept you must POST a YES that I can QUERY to PATH we are standing on.",
    success_response="HORAY! WONDERFUL!",
    failed_response="That is not how you accept a quest! Try again!",
    is_locked_response="That is not how you accept a quest! Try again!",
    is_completed_response="You have already accepted the quest. GET GOING!",

    # execution
    expected_solution="yes",
    execution_strategy="SINGLE_INPUT",
    execution_req_method="POST",

    # parsing
    allowed_req_methods='GET,POST',
    
    expects_query=True,
    query_keys='accept',
    #input_loc="QUERY_DATA",

    # authentication
    auth_type=AuthType.NO_AUTH.value
)