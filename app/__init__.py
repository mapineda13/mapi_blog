from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from database import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mapi_Keyword'
    # Configuracion de DB
    USER_DB = 'postgres'
    PASS_DB = 'an63m0n13'
    URL_DB = 'localhost'
    NAME_DB = 'mapi_blog'
    FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

    app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # inicializar objeto app
    db.init_app(app)

    # configurar flask migrate
    migrate = Migrate()
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    return app
