from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO
from .momentjs import momentjs
from .TCPClient import DataSender

from celery import Celery

import eventlet

eventlet.monkey_patch(socket=True)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
db_shorttrack = SQLAlchemy()

babel = Babel()
dtb = DebugToolbarExtension()
# socketio = SocketIO(message_queue='redis://localhost:6379/0')
socketio = SocketIO(async_mode='eventlet')
# socketio = SocketIO(message_queue='redis://')
# socketio = socketio(message_queue='redis://')

# socketio = SocketIO(message_queue='amqp:///socketio')
celery = Celery('deviceDataHandler', broker='redis://')

# celery = Celery('deviceDataHandler', broker='amqp://')
ScoreboardSender = DataSender()
migrate = Migrate()
migrate_shorttrack = Migrate()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.jinja_env.globals['momentjs'] = momentjs

    babel.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    db_shorttrack.init_app(app)
    login_manager.init_app(app)
    dtb.init_app(app)
    socketio.init_app(app, message_queue='redis://')

    # migrate.init_app(app, db)
    migrate_shorttrack.init_app(app, db_shorttrack)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .raceinfo import raceinfo as raceinfo_blueprint
    app.register_blueprint(raceinfo_blueprint, url_prefix='/raceinfo')

    from .shorttrack import shorttrack as shorttrack_blueprint
    app.register_blueprint(shorttrack_blueprint, url_prefix='/shorttrack')
    return app
