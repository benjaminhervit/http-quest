from app.game.quests.quest_data import QuestData
from app.request_management.request_settings import RequestSettings
from app.game.quests.accept_quest import accept_q

welcome_q = QuestData(
    #TXT
    title="Welcome",
    story_txt="Welcome to a CRUDe game! The (re)quest to claim the CRUDe crown!",
    directions_txt = "you should get here when registering?",
    quest_txt="To get started, simply follow the directions.",
    response_wrong_txt="... You should not even be able to fail this... How???",
    response_correct_txt="We have lucky to have you here.",
    response_completed_txt="What are you even doing here?? Get goin!",
    
    #functions
    correct_answer="",
    quest_validator_type="NONE",
    
    #next
    next_quest_directions = accept_q.directions_txt,
    
    request_settings = RequestSettings(
        req_method='GET',
        answer_location='NONE',
        answer_key='ANSWER',
        auth_type='USERNAME',
        token_location='NONE',
        username_location='PATH'
    )
)