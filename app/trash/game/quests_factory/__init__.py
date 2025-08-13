from app.models import Quest

from app.game.quests_factory.make_welcome_q import make_welcome_q
from app.game.quests_factory.make_accept_q import make_accept_q
from app.game.quests_factory.make_register_q import make_register_q

from app.game.quests_factory.make_null_q import make_null_q #NOT INCLUDED IN GAME


def make_all_quests() -> list[Quest]:
    quests = [make_welcome_q(), make_accept_q(), make_register_q()]
    return quests