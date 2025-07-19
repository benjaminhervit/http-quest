from app.game.quests.quest_data import QuestData
from app.game.quests.empty_quest import empty_quest
from app.request_management.request_settings import RequestSettings

accept_q = QuestData(
    #TXT
    title="Welcome",
    story_txt="You stand in front of a big decision... ish...",
    directions_txt = "POST yes after your name in the PATH to accept this epic reQUEST.",
    quest_txt="To get started, simply follow the directions.",
    response_wrong_txt="That is not how you accept a quest! Try again!",
    response_correct_txt="HORAY! WONDERFUL!",
    response_completed_txt="You have already accepted the quest. GET GOING!",
    
    #functions
    correct_answer="yes",
    quest_validator_type="SINGLE_INPUT",
    
    #next
    next_quest_directions = empty_quest.directions_txt,
    
    request_settings = RequestSettings(
        req_method='POST',
        answer_location='QUERY',
        answer_key='answer',
        auth_type='USERNAME',
        token_location='NONE',
        username_location='PATH'
    )
)