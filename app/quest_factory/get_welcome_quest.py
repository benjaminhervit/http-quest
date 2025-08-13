from app.quest import QuestData
from app.blueprints.quests import bp

def get_welcome_quest():
    return QuestData(
        title="Welcome",
        start_message=("""
                    Welcome reQuest! An epic adventure to claim the CRUDe crown! 
                    But before we begin, you must tell me who you are adventurer?
                    """),
        quest="Extend the path with /your_name",
        locked="",
        completed=("""
                        What a pleasure to meet you [HERO]! Now, I believe in you! I do but...
                        how should I put it... I prefer not to put all my trust in one hero?
                        Better 10 heroes on the roof than one in my pocket?
                        What I mean is that there are other heroes and before you can join the quest,
                        we need you to sign up for... legal and tracking purposes.
                        Like.... not evil tech tracking just... who are you and how far are you in this 
                        quest its really no big deal... It actually sounds much worse now that I am 
                        trying to explain it...
                        """),
        next_path="GET to auth/register for your next instructions.",
        hint="",
        url_prefix=bp.url_prefix if bp.url_prefix else ""
    )