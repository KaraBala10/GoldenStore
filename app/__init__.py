import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_modals import Modal
from flask_mail import Mail
from app.config import Config
from flask_admin import Admin

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate(db)
login_manager = LoginManager()
ckeditor = CKEditor()
modal = Modal()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()
admin = Admin()


def create_app(config_calss=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.adminbp.routes import MyAdminIndexView

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    modal.init_app(app)
    mail.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())

    from app.main.routes import main
    from app.users.routes import users
    from app.items.routes import items
    from app.offers.routes import offers_bp
    # from app.accounts.routes import accounts_bp
    from app.errors.handlers import errors
    from app.adminbp.routes import adminbp

    app.register_blueprint(adminbp)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(items)
    app.register_blueprint(offers_bp)
    # app.register_blueprint(accounts_bp)
    app.register_blueprint(errors)
    return app
