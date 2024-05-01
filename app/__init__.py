import logging
from logging.handlers import RotatingFileHandler
import os

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

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/headloop.log',
                                                maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('HeadloopApp startup')

    return app
