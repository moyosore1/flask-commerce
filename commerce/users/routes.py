from flask import Blueprint, request, jsonify
from commerce import create_app, db, bcrypt
from commerce.users.models import Users
import jwt


users = Blueprint('users', __name__)
# app = create_app()


@users.route('/users')
def hello():
    return ("Hello")


@users.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return "Email already exists"
        else:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = Users(name=data['name'], email=data['email'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"user {new_user.name} has been registered successfully."}


@users.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            token = jwt.encode({'name': user.name,'email': user.email,'userId': user.id}, app.config['SECRET_KEY'])
            return jsonify({'token' : token})
        return "Incorrect Password"