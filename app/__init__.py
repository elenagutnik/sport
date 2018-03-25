from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO
from werkzeug.contrib.cache import MemcachedCache

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
babel = Babel()
dtb = DebugToolbarExtension()
socketio = SocketIO()

cache = MemcachedCache(['127.0.0.1:11211'])

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    babel.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    dtb.init_app(app)
    socketio.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .raceinfo import raceinfo as raceinfo_blueprint
    app.register_blueprint(raceinfo_blueprint, url_prefix='/raceinfo')

    return app
