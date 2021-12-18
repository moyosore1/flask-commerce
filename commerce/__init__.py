from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


from .config import Config

db = SQLAlchemy()


bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
    db.init_app(app)

    bcrypt.init_app(app)

    from commerce.store.routes import store
    from commerce.users.routes import users

    app.register_blueprint(users)
    app.register_blueprint(store)

    # from cbtexam.admin.models import BlacklistToken
    # with app.app_context():
    #     db.create_all()

    return app
