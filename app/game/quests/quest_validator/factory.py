import app.game.quests.quest_validator.strategies as strategies
from app.enums import ValidatorKey

functions = {
    ValidatorKey.NONE : strategies.no_quest
}

def create_quest_validator(_type:str):
    return functions.get(_type)