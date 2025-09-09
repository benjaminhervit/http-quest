from app.quest import QuestData
from app.blueprints.quests import bp


def get_start_quest():
    return QuestData(
        title="Welcome",
        start_message=(
            """
                    Welcome dear {HERO} to... reQuest! An epic adventure to claim the CRUDe crown! 
                    But before we begin, you must tell me: Who you are {HERO}?
                    """
        ),
        quest="To tell me your name, journey onward by adding /your_name to the end of the PATH you see above.",
        locked="",
        completed=(
            """
                        What a pleasure to meet you {HERO}! Now, I believe in you! I do but...
                        how should I put it... I prefer not to put all my trust in one hero?
                        Better 10 heroes on the roof than one in my pocket?
                        What I mean is that there are other heroes and before you can join the quest,
                        we need you to sign up for... legal and tracking purposes.
                        Like.... not evil tech tracking just... who are you and how far are you in this 
                        quest its really no big deal... It actually sounds much worse now that I am 
                        trying to explain it...
                        """
        ),
        next_path="GET to [url]/auth/register",
        hints=["The PATH is the part after the main website name. For example, in domain.com/quest/start the PATH is /quest/start.",
               "Where in your browser would you usually GET to say... a world wide search engine or chat buddy that thinks all your questions are great?"],
        learning="""Great job. The PATH is the part of the that comes after the root URL, e.g. reQuest.com is the root URL. '/game/start' is a PATH.
                    When you added your name name, {HERO}, the PATH became /game/start/{HERO}.
                    The PATH can direct you to certain pages but also include parameters like how you just added your name: {HERO}.
                """,
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
