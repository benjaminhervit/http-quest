from app.errors import GameError
from app.request_management.parsed_request import ParsedRequest

from app.game.quests.quest import Quest
from app.enums import QuestState, StatusCode, ParsingKey, QuestAction

def execute_quest(q:Quest, p:ParsedRequest):
    if q is None:
        raise GameError('Quest was None in gm.execute_quest', code=StatusCode.SERVER_ERROR)
    if p is None:
        raise GameError('Parsed was None in gm.execute_quest', code=StatusCode.SERVER_ERROR)
    
    actions:dict[QuestAction, callable] = {
        QuestAction.GET_QUEST : _get_quest,
        QuestAction.ANSWER : _answer
    }
    
    state:QuestState = _get_state()
    action:QuestAction = _get_action(p)
    
    response:dict = actions.get(action)(quest_obj=q, player=p)
    response['state'] = state.value
    return response

def _get_action(p:ParsedRequest) -> QuestAction:
    try:
        return QuestAction(p.get(ParsingKey.ACTION_TYPE))
    except ValueError as exc:
        raise GameError('Game manager could not recognize player action. Check parsed data.', code=StatusCode.SERVER_ERROR) from exc

def _get_state() -> QuestState:
    return QuestState.UNLOCKED

def _get_quest(**kwargs):
    quest_obj = kwargs.get('quest_obj')
    if quest_obj is None:
        raise GameError('No quest object in get_quest. Developer need to fix this.', code=StatusCode.SERVER_ERROR)
    return {'message':'message from get_quest'}

def _answer(**kwargs):
    quest_obj:Quest = kwargs.get('quest_obj')
    if quest_obj is None:
        raise GameError('No quest object in get_quest. Developer need to fix this.', code=StatusCode.SERVER_ERROR)
    
    correct_answer = quest_obj.correct_answer.lower()
    if correct_answer is None:
        raise GameError('No correct answer in the quest settings. Some dev/designer forgot an important thingy...', code=StatusCode.SERVER_ERROR)
    
    player:ParsedRequest = kwargs.get('player')
    user_answer = player.get(ParsingKey.ANSWER.value)
    if user_answer is None:
        raise GameError('Found no answer for quest answer. This is some dev stuff. ', code=StatusCode.SERVER_ERROR)
    print(f'user:{user_answer} vs quest: {correct_answer}')
    if user_answer == correct_answer:
        return {'message':'Quest completed! Confetty time!'}
    
    return {'message':'The user was wrong!'}