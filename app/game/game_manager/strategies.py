from app.errors import ParsingError, GameError
from app.enums import StatusCode, QuestState, ParserKey, QuestKey
from app.models import User

def none_quest(gm: 'QuestManager') -> bool:
    return True

def accept_quest(qm: 'QuestManager') -> bool:
    from app.game.game_manager.quest_manager import QuestManager
    #hard coded accept_quest solution for now
    
    if not isinstance(qm, QuestManager):
        raise GameError('gm_exec strat did not get GM',
                        code=StatusCode.SERVER_ERROR)
    
    answer = qm.player_inputs[ParserKey.QUERY_DATA]['accept']
    return answer == qm.quest.solution_expected

def register(qm: 'QuestManager') -> bool: 
    from app.game.game_manager.quest_manager import QuestManager
    #hard coded accept_quest solution for now

    if not isinstance(qm, QuestManager):
        raise GameError('gm_exec strat did not get GM',
                        code=StatusCode.SERVER_ERROR)

    inputs = qm.player_inputs.get(ParserKey.FORM_DATA)
    if not inputs:
        raise GameError('Could not find form data / player inputs',
                        code=StatusCode.BAD_REQUEST.value)

    username = inputs.get(ParserKey.USERNAME.value)
    if not username:
        raise GameError(f'Could not find key {ParserKey.USERNAME.value} in form data.',
                        code=StatusCode.BAD_REQUEST.value)
    if User.get_by_username(username=username):
        raise GameError(f'A user with the name {username} already exists.',
                        code=StatusCode.BAD_REQUEST)

    new_user = User(username=username)
    from app.extensions import db
    db.session.add(new_user)
    db.session.commit()

    qm.user = new_user
    print(f"user in QM now: {qm.user}")
    return True
