from app.quest import QuestData


def get_quest():
    return QuestData(
        title="Break the wall on fire",
        locked="I am sorry hero but I cannot allow you in just yet.",
        start_message="""
        Hello {HERO}! I AM... A petty little creature! And this! Is my wall of fire MWHAHAHAH! (A big dramatic, impossible to miss wall on fire is behind the small, odd looking creature... There just absolutely no summetry anywhere in its deform body!). If you want to win the CRUDe crown you will have to break down my wall! But to do so, you will have to show endurance, persistency and patience both in actions - and with my squeeky persona and very personal attacks!
        """,
        quest="""We have to DELETE that wall of fire from existence. And as we all know, the only way to delete a hot wall is through many, small, repeated attacks. This is not something POSTMAN or any other client can handle. This requires reptilian or coffee induced powers (.... it's Python and JavaScript).
        Use Jason as the multi-tool-sledgehammer he is. URL have to DELETE the wall saying in JSON {JSON_KEY}:{JSON_VAL} x {TOTAL_REQS} TIMES! But wait! There is more! Jason does not know his own limits, so he must WAIT AT LEAST {MIN_WAIT} seconds between each attack or he will burn up and you will have to find a new Jason and start over (they are cheap and easy to get their hands on - I bet one will just appear by itself really). BUT WAIT! THERE IS MORE! As we all know, walls of -fuck it - fire walls are self-repairable-ish. DO NOT WAIT LONGER THAN {MAX_WAIT} seconds between each attack or it will have healed itself and consume your Jason out of pure spite and... well same story. Good luck!""",
        completed="""NO—NO, THIS DOESN’T COUNT! YOU SAID IT TOO WELL! I WAS GOING TO CHANGE THE RULES! I WAS THIS CLOSE TO ADDING A HALF-SECOND CLAUSE! 
        GIVE IT BACK! THE CRUDe CROWN IS MINE! MINE!! …sniff 
        You didn’t even struggle the right way…
        FINE. TAKE IT. I NEVER WANTED IT ANYWAY.…
        I’M TELLING EVERYONE THIS WAS BORING.""",
        failed="Well done!",
        next_path="TBD",
        learning="There are two ways that you managed to destroy the wall. Either you did a lot of manually requests - or you have spend much longer time automating it than it would take to just do it manually (WOHO!). We hope you went the coding way because it means you have learned a very crucial skill for your final assignment.",
        xp=1,
        url_prefix="/game",
        hints=["https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers",
               "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Authorization",
               "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type",
               "A approach is to first make a successful request with the HTTP Client so you know all your variables. Then you can start implementing it with code.",
               "This is a great chance to practice repeated http-requests calls to a server with a timer in JavaScript. Something you will need in your later assignments."
               ]
    )
