from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()

def create_app(config_class=Config):
    # app configurations
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    # blueprint configuration
    from app.views.main import main
    app.register_blueprint(main)

    from app.views.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from app.views.errors import errors
    app.register_blueprint(errors)

    return app

from app import models
