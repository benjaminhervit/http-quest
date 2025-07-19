import app.game.quest_validator.strategies as strategies
from app.enums import ValidatorKey

functions = {
    ValidatorKey.NONE : strategies.none_quest,
    ValidatorKey.SINGLE_INPUT : strategies.single_input_validator
}

def create_quest_validator(_type:str):
    return functions.get(_type)