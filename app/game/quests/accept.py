from app.models.quest import Quest
from app.enums import ParserKey, AuthType, QuestExecutionStrategy

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
    is_stateless=True,
    solution_expected="yes",
    solution_location=ParserKey.QUERY_DATA.value,
    solution_key='accept',
    execution_strategy=QuestExecutionStrategy.ACCEPT_QUEST.value,
    execution_req_method="GET",

    # parsing
    allowed_req_methods='GET',
    
    # expects_query=True,
    query_keys='accept',

    # authentication
    auth_type=AuthType.NO_AUTH.value
)