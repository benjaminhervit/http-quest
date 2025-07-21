from app.models.quest import Quest

welcome_Q = Quest(
    title="Welcome",
    story=("Welcome to a CRUDe game! The (re)quest to claim the CRUDe crown!\n"),
    directions="you should get here when registering?",
    quest="Extend this PATH and QUERY YES as your ANSWER to accept the reQUEST for the CRUDe crown!",

    success_response="There is no time to wait! Follow the directions and move forward!",
    failed_response="Here there is no failure. Only a wrong missing ANSWER... and the answer is YES",
    is_locked_response="How did you even get here? This quest is LOCKED! Go back where you came from!",
    is_completed_response="What are you even doing here?? Get goin!",
    
    allowed_req_methods="GET"
)