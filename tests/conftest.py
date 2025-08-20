import pytest
from app.extensions import db
from app import create_app


@pytest.fixture
def app():
    app = create_app()
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
