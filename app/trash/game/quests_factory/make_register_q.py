from app.models.quest import Quest
from app.enums import AuthType, QuestExecutionStrategy


def make_register_q() -> Quest:
    return Quest(
        # content
        title="Register",
        story="To accept the quest - you must first FORM and POST your name\n",
        directions="Go to game/register",
        quest_description="FORM your username and POST it here.",

        # parsing settings
        allowed_req_methods="GET,POST",
        form_keys="username",

        # authentication
        auth_type=AuthType.NO_AUTH.value,

        # exeuction
        is_stateless=True,
        execution_strategy=QuestExecutionStrategy.REGISTER.value,
        execution_req_method="POST",
        success_response="HURRAY!",
        failed_response="Here there is no failure. Only a wrong missing ANSWER... and the answer is YES",
        is_locked_response="How did you even get here? This quest is LOCKED! Go back where you came from!",
        is_completed_response="What are you even doing here?? Get goin!"
    )