from typing import Callable

import app.game.game_manager.strategies as strategies
from app.errors import GameError
from app.enums import QuestExecutionStrategy, ParserKey


functions = {
    QuestExecutionStrategy.AUTO_COMPLETE: strategies.none_quest,
    QuestExecutionStrategy.ACCEPT_QUEST: strategies.accept_quest,
    QuestExecutionStrategy.REGISTER: strategies.register
}


def create_gm_execute_strategy(fn_key: str) -> Callable:
    if fn_key not in QuestExecutionStrategy:
        raise GameError(f'solution_fn key ({fn_key}) not in ValidatorKey enum.')
    fn = functions.get(QuestExecutionStrategy(fn_key))
    if fn is None:
        raise GameError(
            f'No solution_fn for key ({fn}) in create_solution_validator.'
        )
    return fn