from app.quest import QuestData
from app.blueprints.quests.auth import bp

_title = "Registration"

def get_quest_title():
    return _title

def get_quest():
    return QuestData(
        title=_title,
        start_message=(
            """To begin the quest, you must tell us your
                                    name,so that we can follow you on y
                                    our adventures."""
        ),
        quest=(
            """FORM username:your_name and POST to auth/register
                        or... you know... just use the form below?"""
        ),
        locked="",
        completed=(
            """
                            Thank you {HERO}! Now, you are ready!",
                            Finally, someone with a heroic name as {HERO}
                            cannot fail! Move on! 
                            REEEEEMEMBEEEER to aaaalwaaaayyyyys 
                            keep your name in your head at all times.
                            """
        ),
        next_path=("GET to /game/identify-yourself"),
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
