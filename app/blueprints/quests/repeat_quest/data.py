from app.quest import QuestData


def get_quest():
    return QuestData(
        title="Three its the magic number",
        locked="I am sorry hero but I cannot allow you in just yet.",
        start_message="""
        Hello {HERO}! I AM.... A petty little creature - but if you can handle my impatience and micro-management - then you have earned the CRUDe Crown! Your time has already begun!
        """,
        quest="Make Jason say:\"please give my hero the crude crown\" ... {TOTAL_REQS} TIMES! But wait! There is more! He has to wait at least {MIN_WAIT} seconds and at most {MAX_WAIT} seconds between each please. If he fails - I will reset his please streak - and you must start over... MWAHAHAHHAHA!",
        completed="""NO—NO, THIS DOESN’T COUNT! YOU SAID IT TOO WELL! I WAS GOING TO CHANGE THE RULES! I WAS THIS CLOSE TO ADDING A HALF-SECOND CLAUSE! 
        GIVE IT BACK! THE CRUDe CROWN IS MINE! MINE!! …sniff 
        You didn’t even struggle the right way…
        FINE. TAKE IT. I NEVER WANTED IT ANYWAY.…
        I’M TELLING EVERYONE THIS WAS BORING.""",
        failed="Well done! Just {REQ_LEFT} to go!",
        next_path="TBD",
        learning="There are two ways that you have completed this level. Either you A) Have been sending the same message manually 100 times (zzzzz) or you have B) spend longer time automating it than it would take to just do it manually (WOHO!). We hope you went the coding way because it means you have learned a very crucial skill for your final assignment.",
        xp=1,
        url_prefix="/game",
        hints=["https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers",
               "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Authorization",
               "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type"]
    )
