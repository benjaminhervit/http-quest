from app.models.quest import Quest
from app.enums import QuestExecutionStrategy, AuthType


def make_null_q() -> Quest:
    return Quest(
        # content
        title="",
        story="",
        directions="There is nothing from here. This is an empty path.",
        quest_description="",

        # parsing
        allowed_req_methods="GET",
        # expects_query=False,

        # authentication
        auth_type=AuthType.NO_AUTH.value,

        # execution
        is_stateless=True,
        execution_strategy=QuestExecutionStrategy.AUTO_COMPLETE.value,
        execution_req_method="GET"
    )
