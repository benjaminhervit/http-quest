
from app.models import Quest
from app.game.quests_factory.make_register_q import make_register_q
from app import utils
from app.enums import QuestKey, AuthType


def test_get_quest(app):
    with app.app_context():
        # when getting quest by slur 'register' Q3 is returned
        quest: Quest | None = Quest.get_by_slug('register')
        assert isinstance(quest, Quest)
        assert quest.title == 'Register'
        assert quest.slug == 'register'


def test_quest_req_methods():
    q = make_register_q()
    # valid methods
    assert q.allowed_req_methods == 'GET,POST'
    # execution req for validating user input
    assert q.execution_req_method == 'POST'


def test_form_keys_has_username(app):
    q = make_register_q()
    valid_keys = utils.get_enum_values_as_list(QuestKey)
    assert q.form_keys in valid_keys
    assert q.form_keys == 'username'
    assert q.form_keys == QuestKey.USERNAME.value


def test_only_form_expects_data(app):
    q = make_register_q()
    assert q.query_keys is None
    assert q.form_keys is not None


def test_no_auth():
    q = make_register_q()
    assert q.auth_type is AuthType.NO_AUTH.value
