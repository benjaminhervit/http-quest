from app.game.quests.quest_data import QuestData
from app.game.quests.empty_quest import empty_quest

welcome_q = QuestData(
    #TXT
    title="Welcome",
    welcome_txt="Welcome to a CRUDe game!",
    directions_txt = "JUST GET HERE ALREADY!",
    description_txt="I should probally say something inspiring here",
    quest_txt="POST your name in the PATH you are treading and I will let you pass.",
    response_wrong_txt="Absolutely wrong - I mean.. not even close! HOLY!",
    response_correct_txt="BEHOLD! OUR SAVIOR IS HERE!",
    response_completed_txt="What are you even doing here?? Get goin!",
    
    #functions
    correct_answer="test_answer",
    quest_validator_type="NONE",
    
    #next
    next_quest = empty_quest,
    
    request_settings = {
        "METHOD_TYPE":"GET",
        "AUTH_TYPE" : "USERNAME",
        "USERNAME_LOCATION" : "PATH",
        "TOKEN_LOCATION" : "NONE",
        "CONTENT_LOCATION" : "NONE",
        "EXPECTED_FIELDS" : ["USERNAME", "AUTHTYPE"]
    }
)