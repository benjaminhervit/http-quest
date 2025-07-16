from app.game.quests.quest_data import QuestData
from app.game.quests.empty_quest import empty_quest

welcome_q = QuestData(
    title="Welcome",
    welcome_txt="Welcome to a CRUDe game!",
    directions_txt = "JUST GET HERE ALREADY!",
    description_txt="I should probally say something inspiring here",
    quest_txt="POST your name in the PATH you are treading and I will let you pass.",
    correct_answer="test_answer",
    response_wrong_txt="Absolutely wrong - I mean.. not even close! HOLY!",
    response_correct_txt="BEHOLD! OUR SAVIOR IS HERE!",
    response_completed_txt="What are you even doing here?? Get goin!",
    next_quest = empty_quest,
    
    request_settings = {
        'GET': {
            "REQ_TYPE" : "GET_QUEST",
            "AUTH_TYPE" : "USERNAME",
            "USERNAME" : "PATH",
            "CORRECT_ANSWER" : "",
            "EXPECTED_FIELDS" : ["USERNAME"]
        },
        'POST': {
            "REQ_TYPE" : "ANSWER",
            "ANSWER" : "QUERY",
            "USERNAME" : "PATH",
            "AUTH_TYPE" : "USERNAME",
            "CORRECT_ANSWER" : "TEST",
            "EXPECTED_FIELDS" : ["USERNAME","ANSWER"]
        }
    },
    
    answer_settings= {
    }
)