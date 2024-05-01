from flask import Flask
from config import Config

def create_app(config_class=Config, test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
