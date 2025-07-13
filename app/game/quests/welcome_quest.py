from app.game.quests.quest import Quest
from app.request_handler.enums import RequestEnums as RE

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

welcome_q = Quest(
    title="Welcome",
    welcome_text="Welcome to a CRUDe game!",
    description="I should probally say something inspiring here",
    quest="POST your name in the PATH you are treading and I will let you pass.",
    answer="test_answer",
    response_wrong="Absolutely wrong - I mean.. not even close! HOLY!",
    response_correct="BEHOLD! OUR SAVIOR IS HERE!",
    response_completed="What are you even doing here?? Get goin!",
    next_quest_directions="... yearh.... i should really tell yout something here right?",
    request_settings={
        RE.GET: {
            RE.BODY_TYPE: RE.PATH,
            RE.AUTH_TYPE: RE.AUTH_BY_USERNAME,
            RE.USERNAME_LOCATION: RE.PATH,
        }
    }
)