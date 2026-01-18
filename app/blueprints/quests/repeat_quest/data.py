from app.quest import QuestData


def get_quest():
    return QuestData(
        title="Three its the magic number",
        locked="I am sorry hero but I cannot allow you in just yet.",
        start_message="""
        Hello {HERO}! This time you must beg... yes... beg. Beg to pass! MWAHAHAHAHA!
        """,
        quest="Make Jason say:please! 100 TIMES but-no-more-than-one-beg-a-second-to-not-overload-my-poor-little-attentionspan.",
        completed="Wauw okay! Relax! Jesus! How desperate you??? Move along!",
        failed="",
        next_path="TBD",
        learning="There are two ways that you have completed this level. Either you A) Have been sending the same message manually 100 times (zzzzz) or you have B) spend longer time automating it than it would take to just do it manually (WOHO!). We hope you went the coding way because it means you have learned a very crucial skill for your final assignment.",
        xp=1,
        url_prefix="/game",
    )
