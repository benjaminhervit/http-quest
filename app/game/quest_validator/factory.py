import app.game.quest_validator.strategies as strategies
from app.enums import ValidatorKey
from app.errors import GameError
from typing import Callable

functions = {
    ValidatorKey.NONE: strategies.none_quest,
    ValidatorKey.SINGLE_INPUT: strategies.single_input_validator
}

def create_solution_validator(_type: str) -> Callable | None:
    if _type not in ValidatorKey:
        raise GameError(f'solution_fn key ({_type}) not in ValidatorKey enum.')
    fn = functions.get(ValidatorKey(_type))
    if fn is None:
        raise GameError(
            f'No solution_fn for key ({_type}) in create_solution_validator.'
        )
    return functions.get(ValidatorKey(_type))