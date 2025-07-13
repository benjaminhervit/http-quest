from app.game.quests.quest import Quest
from app.request_handler.enums import RequestEnums as RE

first_q = Quest(
    title="The First Test",
    welcome_text="Welcome to a CRUDe game!",
    description="You stand in front of an old wise sage who, without considering if you are actually listening, begins to speak: ",
    quest='To know that you are worthy, you must answer: Answer to the Ultimate Question of Life, The Universe, and Everything? When you have an answer, POST it in the path after your name',
    answer="test_answer",
    response_wrong="Absolutely wrong - I mean.. not even close! HOLY!",
    response_correct="That is correct! You are truly enlightened! Alas, if only we knew had known what the Ultimate Question of Life, the Universe, and Everything is - but there is not time! Something is approaching that only you can fix!",
    response_completed="What are you even doing here?? Get goin!",
    next_quest_directions="... yearh.... i should really tell yout something here right?",
    request_settings={
        'GET': {
            RE.BODY_TYPE: RE.PATH,
            RE.AUTH_TYPE: RE.AUTH_BY_USERNAME,
            RE.USERNAME_LOCATION: RE.PATH,
        },
        'POST':{
            RE.BODY_TYPE: RE.PATH,
            RE.AUTH_TYPE: RE.AUTH_BY_USERNAME,
            RE.USERNAME_LOCATION: RE.PATH
        }
    }
)