
from app.quest import QuestData
    def get_quest():
        return QuestData(
            title="delete_wall",
            start_message="",
            quest="",
            completed="",
            locked="",
            next_path="",
            hints=[],
            xp=1,
            url_prefix="/game"
        )
