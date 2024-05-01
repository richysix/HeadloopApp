import pytest

from app import create_app

@pytest.fixture
def test_app():
    app = create_app(test_config = {
        'TESTING': True,
        'SECRET_KEY': 'dev',
    })
    return app

@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def runner(test_app):
    return test_app.test_cli_runner()