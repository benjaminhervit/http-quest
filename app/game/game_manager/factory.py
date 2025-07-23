from app.models import Quest, User, UserQuestState
from app.enums import ParserKey, StatusCode
from app.errors import ParsingError
from app.game.game_manager.game_manager import GameManager

def create_game_manager(quest: Quest, req_data: dict):
    if quest.is_stateless and not quest.username_loc:
        return GameManager(quest, req_data, None, None)
    
    username = req_data.get(ParserKey.USERNAME)
    if not username:
        raise ParsingError('Could not find username in parsed request.',
                           code=StatusCode.SERVER_ERROR)
    profile = User.get_by_username(username)
    if not profile:
        raise ParsingError(f'Could not find profile for username {username}',
                           code=StatusCode.BAD_REQUEST)
    
    if quest.is_stateless:
        return GameManager(quest, req_data, profile, None)
    
    state = UserQuestState.get_uqs(username, quest.slug)
    if not state:
        raise ParsingError(f'Could not find state for player {username}'
                           f' and quest {quest.title}')
        
    return GameManager(quest, req_data, profile, state.state)