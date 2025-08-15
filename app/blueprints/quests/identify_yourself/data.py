from app.quest import QuestData
from app.blueprints.quests import bp


def get_quest():
    return QuestData(
        title="Identify yourself!",
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
            POST to this path and while you hold your username
            in your HEAD(ers) with AUTHORIZATION.
            """
        ),
        locked="",
        completed=(
            """
                Did I not know better, I would think you had telekinetic powers [HERO].
                Now you know our secret ways of telling friend from enemy! Onwards!
                """
        ),
        next_path=(
            """
                GET to /game/hire_jason
                """
        ),
        hint="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Authorization",
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
