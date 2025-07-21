from typing import Callable

import app.game.quest_validator.strategies as strategies
from app.errors import GameError
from app.enums import SolutionFunc, ParserKey


functions = {
    SolutionFunc.NONE: strategies.none_quest
}

def create_solution_validator(fn_key: str) -> Callable:
    if fn_key not in SolutionFunc:
        raise GameError(f'solution_fn key ({fn_key}) not in ValidatorKey enum.')
    fn = functions.get(SolutionFunc(fn_key))
    if fn is None:
        raise GameError(
            f'No solution_fn for key ({fn}) in create_solution_validator.'
        )
    return fn