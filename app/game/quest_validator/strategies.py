from app.errors import ParsingError, GameError
from app.enums import StatusCode, QuestState
from app.game.game_manager import GameManager

def none_quest(GM: GameManager):
    # None quest will autocomplete or do nothing
    if GM.state == QuestState.UNLOCKED:
        GM.set_state(QuestState.COMPLETED)

def much_match(*args, **kwargs):
    user_input = kwargs.get('user_input')
    expected = kwargs.get('validation_data')
    if user_input is None or expected is None:
        raise ParsingError(f'missing keys in kwargs: {kwargs}. input:{user_input}, exp:{expected}', code=StatusCode.SERVER_ERROR)
    
    return user_input == expected