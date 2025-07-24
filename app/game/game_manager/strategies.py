from app.errors import ParsingError, GameError
from app.enums import StatusCode, QuestState, ParserKey

def none_quest(gm: 'GameManager') -> bool:
    return True

def accept_quest(gm: 'GameManager') -> bool:
    from app.game.game_manager.quest_manager import QuestManager
    #hard coded accept_quest solution for now
    
    if not isinstance(gm, QuestManager):
        raise GameError('gm_exec strat did not get GM',
                        code=StatusCode.SERVER_ERROR)
    
    answer = gm.player_inputs[ParserKey.QUERY_DATA]['accept']
    return answer == gm.quest.expected_solution