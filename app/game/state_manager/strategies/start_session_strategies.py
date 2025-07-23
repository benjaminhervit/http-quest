from app.models import User, Quest, UserQuestState
from app.enums import QuestState, StatusCode
from app.errors import GameError

def get_stateless_start(quest: Quest, user: User) -> QuestState:
    return QuestState.UNLOCKED

def get_state_by_user_quest(quest: Quest, user: User) -> QuestState:
    if not user:
        raise GameError(f'Cannot set state of quest {quest.title}'
                        f'without user', code=StatusCode.BAD_REQUEST)
    
    if not isinstance(user, User):
        raise GameError('user is not User obj',
                        code=StatusCode.SERVER_ERROR)

    uqs = UserQuestState.get_uqs(username=user.username,
                                 slug=quest.slug)
    
    if not uqs:
        raise GameError(f'No UQS for Quest {quest.title} '
                        f'and user {user.username}',
                        code=StatusCode.SERVER_ERROR)
            
    return uqs.state