from enum import Enum
#inspired by https://www.w3.org/Protocols/HTTP/HTRESP.html
class LevelEnum(Enum):
    LEADERBOARD = "leaderboard"
    REGISTRATION = "registration"
    THE_TEST = "the_test"
    THE_MONSTER = "the_monster"
    THE_GATE = "the_gate"
    THE_THRONE_ROOM = "the_throne"
    THE_CROWN = "the_crown"
    SPEAK_TO_JASON = "hason"
    GAME_OVER = "game_over"