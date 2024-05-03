import pytest

from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'dev'

@pytest.fixture
def test_app():
    app = create_app(config_class = TestConfig)
    return app

@pytest.fixture
def client(test_app):
    return test_app.test_client()
