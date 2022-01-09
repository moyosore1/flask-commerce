from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS


db = SQLAlchemy()

bcrypt = Bcrypt()


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

    app.register_blueprint(users)
    app.register_blueprint(store)

    from commerce.users.models import Users
    # with app.app_context():
    #     db.create_all()

    return app
