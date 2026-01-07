from app.quest import QuestData
from app.blueprints.quests import bp

_title = "Identify yourself!"


def get_quest_title():
    return _title


def get_quest():
    return QuestData(
        title=_title,
        quest=(
            """
            GET back to me when you know have learned how to AUTHORIZE yourself with your name. Just use your HEAD(ers).
            """
        ),
        locked="",
        completed=(
            """
                Did I not know better, I would think you had telekinetic powers {HERO}.
                Now you know our secret ways of telling friend from enemy! Onwards!
            """
        ),
        start_message=(
            """
                Oh, I am sorry but I cannot let you pass without seeing some AUTHORIZATION.
                If you are here, I guess that you have already signed up but from here on you must always keep your name in your HEAD(ers) so that we can AUTHORIZE you.
                It's a little telekinetic trick we are using because we don't want to write down their name on the BODY(ies?) all the time.
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
            "If you have your client and authorization working - maybe it is because you are not taking nothing seriously enough..."
        ],
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
