import app.game.state_manager.strategies.start_session_strategies as stat_strat
import app.game.state_manager.strategies.end_session_strategies as end_strat
import app.game.state_manager.strategies.update_state_in_db_strategies as db_strat

from app.game.state_manager.state_manager import StateManager

def create_state_manager(is_stateless: bool):
    if is_stateless:
        return StateManager(stat_strat.get_stateless_start,
                            end_strat.set_closed,
                            db_strat.no_update)
    
    return StateManager(stat_strat.get_state_by_user_quest,
                        end_strat.set_by_active_state,
                        db_strat.update_with_new_state)