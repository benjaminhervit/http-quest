from app.quest import QuestData
from app.blueprints.auth import bp


def get_signup_quest():
    return QuestData(
        title="Registration",
        start_message=("""To begin the quest, you must tell us your
                                    name,so that we can follow you on y
                                    our adventures."""),
        quest=("""FORM username:your_name and POST to auth/register
                        or... you know... just use the form below?"""),
        locked="",
        completed=("""
                            Thank you [HERO]! Now, you are ready!",
                            Finally, someone with a heroic name as [HERO]
                            cannot fail! Move on! 
                            REEEEEMEMBEEEER to aaaalwaaaayyyyys 
                            keep your name in your head at all times.
                            """),
        next_path=("""
                            GET to /hire_jason as fast as you can.
                            This is a skill that you cannot 
                            ignore if you want to succeed!
                            """),
        hint="",
        url_prefix=bp.url_prefix if bp.url_prefix else ""
    )