from app.quest import QuestData


def get_quest():
    return QuestData(
        title="Hire Jason",
        locked="I am sorry hero but I cannot allow you in just yet.",
        start_message="""
        Hello {HERO}! Pleased to meet you! I am... who gives a sh- I got a great squire for you!
        Meet: Jason! Jason can do all sorts of tricks for you - but you need to speak to him in his own language.
        """,
        quest="POST jason:hired in Jasons mother toungue also known as... yes... json...",
        completed="ALRIGHTY OH! Jasons screams and charges ahead. He does not really seem to care what orders he gets...",
        next_path="TBD",
        learning="",
        xp=1,
        url_prefix="/game",
    )
