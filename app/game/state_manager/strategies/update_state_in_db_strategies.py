from app.models import UserQuestState
from app.errors import GameError
from app.enums import StatusCode


def no_update(new_state: str, username: str, slug: str):
    return True


def update_with_new_state(new_state: str, username: str, slug: str):
    uqs = UserQuestState.get_uqs(username, slug)
    if not uqs:
        raise GameError(f'Could not find UQS for username ({username})'
                        f' and slug ({slug})', code=StatusCode.SERVER_ERROR)
    
    UserQuestState.update_state(new_state, uqs)
    return True