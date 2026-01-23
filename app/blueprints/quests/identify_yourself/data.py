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
                GET to /game/hire-jason where a great ally awaits.
            """
        ),
        learning="Most websites and services requires you to use the Authorization header so that they can verify who you are and decide if they want to give you access. For simplicity, we are just asking you to write your username BUT that is NOT SAFE and it is NOT A STANDARD! Usually it is some long gibberish key or token that is build with cryptography and other kinds of mathgic which is not important to us in this course. Just... REMEMBER NEVER TO DO IT HOW WE DID IT HERE IF YOU ARE MAKING A PUSHING SOMETHING TO REAL PRODUCTION ONE DAY!",
        hints=[
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Authorization",
            "https://www.postman.com/",
            "Your web browser cannot do custom authorization. You should look into HTTP Clients or POSTMAN  - or start making requests in Python or JavaScript? Though that might be overkill right now."
        ],
        xp=1,
        url_prefix=bp.url_prefix if bp.url_prefix else "",
    )
