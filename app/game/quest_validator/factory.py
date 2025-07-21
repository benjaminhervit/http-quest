import app.game.quest_validator.strategies as strategies
from app.errors import GameError
from typing import Callable

functions = {
    'NONE': strategies.none_quest,
    'SINGLE_INPUT': strategies.single_input_validator
}

def create_solution_validator(_type: str) -> Callable | None:
    # if _type not in ValidatorKey:
    #     raise GameError(f'solution_fn key ({_type}) not in ValidatorKey enum.')
    fn = functions.get(_type)
    if fn is None:
        raise GameError(
            f'No solution_fn for key ({_type}) in create_solution_validator.'
        )
    return fn