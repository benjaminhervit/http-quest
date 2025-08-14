import pytest
from app.extensions import db
from app.setup import create_and_seed_app
from app.config import TestingConfig


@pytest.fixture
def app():
    app = create_and_seed_app(TestingConfig)
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
