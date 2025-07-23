from app.models.quest import Quest
from app.enums import QuestExecutionStrategy, AuthType

null_Q = Quest(
    # content
    title="",
    story="",
    directions="There is nothing from here. This is an empty path.",
    quest_description="",

    # parsing
    allowed_req_methods="GET",
    expects_query=False,

    # authentication
    auth_type=AuthType.NO_AUTH.value,

    # execution
    execution_strategy=QuestExecutionStrategy.NONE.value,
    execution_req_method="GET"
)
