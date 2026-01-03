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
                            What were we talking about? Oh well! But try heading to the /leaderboard. I think you can see yourself there now?
                            REMEMBER TO CHECK THE NEXT_PATH BEFORE YOU LEAVE!
                            """
        ),
        next_path=("GET to /game/identify-yourself"),
        learning="In this quest you used FORM and POST to send your username to the backend. If you did it from the browser, you can inspec the website and find the form in the HTML. When we ask the data to create something new, we use POST.",
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
