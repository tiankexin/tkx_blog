from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from app.settings import Config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    # config[config_name].init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .views.auth.view import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

