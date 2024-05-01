from flask import Flask, render_template
from config import Config

def not_found_error(error):
    return render_template('404.html'), 404

def create_app(config_class=Config, test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.register_error_handler(404, not_found_error)

    return app
