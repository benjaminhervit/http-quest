from app.errors import GameError
from app.request_management.parser.parsed_request import ParsedRequest

from app.game.quests.quest_data import QuestData
from app.game.quests.quest_session import QuestSession
from app.enums import QuestState, StatusCode, QuestDataKey, PlayerAction

def execute_quest(q:QuestData, p:ParsedRequest):
    if q is None:
        raise GameError('Quest was None in gm.execute_quest', code=StatusCode.SERVER_ERROR)
    if p is None:
        raise GameError('Parsed was None in gm.execute_quest', code=StatusCode.SERVER_ERROR)

    username = p.get(QuestDataKey.USERNAME.value)
    answer = p.get(QuestDataKey.ANSWER.value)
    player_action = _get_action(p)
    state:QuestState = _get_quest_state()
    session = QuestSession(username=username, player_answer=answer, quest_state=state, quest=q, player_action=player_action)
    return session.get_response()

def _get_action(p:ParsedRequest) -> PlayerAction:
    try:
        return PlayerAction(p.get(QuestDataKey.ACTION_TYPE))
    except ValueError as exc:
        raise GameError('Game manager could not recognize player action. Check parsed data.', code=StatusCode.SERVER_ERROR) from exc

def _get_quest_state() -> QuestState:
    return QuestState.UNLOCKED