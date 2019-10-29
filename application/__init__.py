# standard library
import os
import logging
from logging.handlers import RotatingFileHandler

# flask extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# microblog
from config import Config

# instantiate extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ''
login.login_message_category = 'info'
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # from application.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    from application.reports import bp as reports_bp
    app.register_blueprint(reports_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/storylines.log',
                                           maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s:\
             %(message)s [in %(pathname)s%(lineno)d]')
        )

        app.logger.setLevel(logging.INFO)
        try:
            file_handler.setLevel(app.config['LOGGING_LEVEL'])
            app.logger.info('General Logging set at ' +
                            str(app.config['LOGGING_LEVEL']))
        except ValueError as e:
            app.logger.error('Application Configuration Error:' +
                             str(e) + ' is not a valid logging level')
            file_handler.setLevel(logging.INFO)
            app.logger.info('Overriding log configuration to INFO')
        app.logger.addHandler(file_handler)

        app.logger.info('Our Storylines... starting up...')

    return app
