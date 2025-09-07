from app.quest import QuestData
from app.blueprints.quests.auth import bp

_title = "Registration"


def get_quest_title():
    return _title


def get_quest():
    return QuestData(
        title=_title,
        start_message=(
            """Ah... I am glad you made it here {HERO}. To begin the quest, you must tell us your
            name (again yes). We got some... ehm... trust issues, so prefer to know who our heroes are."""
        ),
        quest=(
            """FORM username:your_name and POST to auth/register
                        or... you know... just use the form below?"""
        ),
        locked="",
        completed=(
            """
                            Thank you {HERO}! Now, you are ready!,
                            Finally, someone with a heroic name as {HERO}
                            cannot fail! .... {HERO}... {HERO}...{HERO}{HERO} ....
                            {HERO}{HERO}{HERO}{HERO}{HERO}{HERO}. It has a certain ring to it the more I say it.  Try it?
                            {HERO}{HERO}{HERO}{HERO}{HERO}{HERO}{HERO}{HERO}{HERO}{HERO}{HERO}{HERO}....
                            What were we talking about?
                            """
        ),
        next_path=("GET to /game/identify-yourself"),
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
