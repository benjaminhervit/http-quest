from app.errors import ParsingError, GameError
from app.enums import StatusCode, QuestState

def none_quest(gm: 'GameManager') -> None:
    # None quest will autocomplete or do nothing
    from app.game.game_manager.game_manager import GameManager
    if not isinstance(gm, GameManager):
        raise GameError(f'none_quest() did not receive the GM but instead type: {type(gm)}: {gm}')
    if gm.state == QuestState.UNLOCKED:
        gm.set_state(QuestState.COMPLETED)

def much_match(*args, **kwargs):
    user_input = kwargs.get('user_input')
    expected = kwargs.get('validation_data')
    if user_input is None or expected is None:
        raise ParsingError(f'missing keys in kwargs: {kwargs}. input:{user_input}, exp:{expected}', code=StatusCode.SERVER_ERROR)
    
    return user_input == expected