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
        quest="To tell me your name, URL have to extend the PATH with /your_name.",
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
        next_path="GET to the next quest by replacing the PATH with /auth/register.",
        hints=["The PATH is the part after the main website name. For example, in domain.com/quest/start the PATH is /quest/start.",
               "Where in your browser would you usually GET to say... a world wide search engine or chat buddy that thinks all your questions are great?",
               "Think outside the neon-box. The PATH should hang around in a bar above all this neon."],
        learning="""Great job. The PATH is the part of the that comes after the root URL, e.g. reQuest.com is the root URL. '/game/start' is a PATH.
                    The PATH can direct you to certain pages but it can also include parameters like how you just added your name: {HERO}.
                    /game/start/{HERO} means the backend will read the last part as a value. It is the same thing you are (or have to do) with your Flask routes.
                """,
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
