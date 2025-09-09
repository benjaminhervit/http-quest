from app.quest import QuestData
from app.blueprints.quests import bp

_title = "Identify yourself!"


def get_quest_title():
    return _title


def get_quest():
    return QuestData(
        title=_title,
        start_message=(
            """
                    Okay. You should have signed up for the quest by now
                    - but wee need a way to know who you are. Therefore, 
                    on every new PATH you take from hereon now, you must always
                    identify yourself with AUTHORITY. Otherwise, we will not let you pass.
                    It also means... time to get out of the browser and into a client."""
        ),
        quest=(
            """
            With your name as AUTHORIZATION in your HEAD(ers), POST nothing to this PATH. WARNING! Things are about to get ugly.
            """
        ),
        locked="",
        completed=(
            """
                Did I not know better, I would think you had telekinetic powers {HERO}.
                Now you know our secret ways of telling friend from enemy! Onwards!
                """
        ),
        next_path=(
            """
                GET to /game/hire_jason
                """
        ),
        learning="",
        hints=[
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Authorization",
            "https://www.postman.com/",
        ],
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
