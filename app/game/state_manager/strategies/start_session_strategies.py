from app.models import User, Quest, UserQuestState
from app.enums import QuestState, StatusCode
from app.errors import GameError

def get_stateless_start(quest: Quest, user: User | None) -> QuestState:
    if not isinstance(quest, Quest):
        raise ValueError(f'quest ({quest}) var is not Quest obj.')
    if not quest.is_stateless:
        raise GameError(f'Trying to make stateless start on quest {quest.title}'
                        'which is not stateless.')
    
    return QuestState.COMPLETED

def get_state_by_user_quest(quest: Quest, user: User | None) -> QuestState:
    if not isinstance(quest, Quest):
        raise ValueError(f'quest ({quest}) var is not Quest obj.')
    
    if not isinstance(user, User):
        raise ValueError(f'Cannot set state of quest {quest.title}'
                         f'without user')
        
    if not user.username:
        raise ValueError(f'No username found in user: {user}')

    uqs = UserQuestState.get_uqs(username=user.username,
                                 slug=quest.slug)
    
    if not uqs:
        raise GameError(f'No UQS for Quest {quest.title} '
                        f'and user {user.username}',
                        code=StatusCode.SERVER_ERROR)
    return uqs.state
