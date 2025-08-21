import pytest

from app.quest import QuestData
from app.enums import ContentKeys, QuestState
import app.utils.content_generator as cont_gen


def test_format_string():
    # when one param and correct formatter, then correct formatting
    s = "Test {HERO}"
    s = cont_gen.format_string(s, {"HERO": "Player"})
    assert s == "Test Player"

    # when multi params and correct formatter, then correct formatting
    s = "Test {HERO} is {FOO} but still {HERO}"
    s = cont_gen.format_string(s, {"HERO": "Player", "FOO": "BAR"})
    assert s == "Test Player is BAR but still Player"

    # when HERO is not param, then it is not changed
    s = "Test HERO"
    s = cont_gen.format_string(s, {"HERO": "Player"})
    assert s == "Test HERO"

    # when no formatting passed, then no changes
    s = "Test {HERO}"
    with pytest.raises(ValueError, match="formatting cannot by falsy: \{\}"):
        s = cont_gen.format_string(s, {})
    # assert s == "Test HERO"
