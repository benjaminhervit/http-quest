import pytest
from flask import Flask

from app import create_app
from app.extensions import db
from app.config import TestingConfig
from app.models.user import User
from app.models.quest import Quest
from app.game.quests import quests
from app.game.quests.welcome import welcome_Q
from app.game.quests.accept import accept_Q

@pytest.fixture
def app():
    app: Flask = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        db.session.add_all(quests)

        accept_Q.prev_quest_id = welcome_Q.id
        db.session.commit()

        db.session.add(User(username="test_user"))
        db.session.commit()

        yield app

        db.drop_all()

@pytest.fixture
def test_client(app):
    return app.test_client()