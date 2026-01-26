from app.quest import QuestData


def get_quest():
    return QuestData(
        title="Hire Jason",
        locked="I am sorry hero but I cannot allow you in just yet.",
        start_message="""
        Hello {HERO}! Pleased to meet you! I am... who gives a sh- I got a great squire for you!
        Meet: Jason! Jason can do all sorts of tricks for you. Mostly giving and receiving messages with to other characters.
        As it turns out, almost everyone here has their own Jason to speak on their behalf.
        You want to pass on a message to someone? Let Jason do it. 
        They want to tell you something? You can be almost certain they will let a Jason do the job.
        There is just two things you have to learn: 
        1) how to speak Json (yes the language of the Jasons are Json because it is cheaper when printing signs and badges).
        2) How to get into your HEAD(ers) that you are sending Jason.
        ... And you are good to go!
        """,
        quest="In JASON, URL have to make ONE POST to this PATH with 'jason_you_are:hired' and 'now:march ahead!'.",
        completed="ALRIGHTY OH! Jasons screams and charges ahead. He does not really seem to consider the consequences of the orders your give him. But now that you have Jason by your side, you are ready to face: the annoying creature.",
        next_path="GET on the PATH to the /game/the-wall-on-fire to face the final challenge.",
        learning="""Great job! This quest was all about getting familiar with sending JSON in a request. 
        Odds are, you are reading this as a JSON response as well.
        For most use cases this is an easy and human-friendly (yes it is) way to structure and share data that are more flexible than FORMs.
        The most annoying thing is that we cannot control the order of the key entries in JSON, so I guess some of you are irritated by this when reading all these long ramblings - and that's fair...
        Luckily that is something you can fix yourself! 
        BONUS QUEST (No experience or progression for doing it - just learning): 
        Try to make a request from JavaScript or Python and when you get this back: print it in this key order: title, status, story, quest, hints, nex_path. REMEMBER TO CHECK IF THEY KEYS EXISTS BEFORE PRINTING!
        """,
        hints=["Here is how to speak Jason 101: https://www.w3schools.com/js/js_json_syntax.asp",
               "How to get Jason into your HEAD(ers): https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type"
                ],
        xp=5,
        url_prefix="/game",
    )
