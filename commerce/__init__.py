import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

import cloudinary


db = SQLAlchemy()

bcrypt = Bcrypt()


cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)


def create_app(config=None):
    app = Flask(__name__)
    if app.config['ENV'] == 'production':
        app.config.from_object('config.Production')

    else:
        app.config.from_object('config.Development')

    db.init_app(app)

    bcrypt.init_app(app)

    CORS(app, supports_credentials=True)

    from commerce.store.routes import store
    from commerce.users.routes import users
    from commerce.admin.routes import admin

    app.register_blueprint(users)
    app.register_blueprint(store, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/api')

    from commerce.users.models import Users
    from commerce.store.models import Product, Category, Order, OrderItem
    from commerce.admin.models import Admin

    return app
