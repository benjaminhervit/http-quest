from app.game.quests.quest import Quest
from app.enums import InputLocation, QuestAction, AuthType

welcome_q = Quest(
    title="Welcome",
    welcome_text="Welcome to a CRUDe game!",
    directions = "JUST GET HERE ALREADY!",
    description="I should probally say something inspiring here",
    quest="POST your name in the PATH you are treading and I will let you pass.",
    correct_answer="test_answer",
    response_wrong="Absolutely wrong - I mean.. not even close! HOLY!",
    response_correct="BEHOLD! OUR SAVIOR IS HERE!",
    response_completed="What are you even doing here?? Get goin!",
    next_quest_directions="... yearh.... i should really tell yout something here right?",
    
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