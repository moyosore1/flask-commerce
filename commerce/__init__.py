import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import cloudinary as Cloud


from .config import Config

db = SQLAlchemy()


bcrypt = Bcrypt()

Cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mydb.db'
    db.init_app(app)

    bcrypt.init_app(app)

    from commerce.store.routes import store
    from commerce.users.routes import users

    app.register_blueprint(users)
    app.register_blueprint(store)

    from commerce.store.models import Product
    with app.app_context():
        db.create_all()

    return app
