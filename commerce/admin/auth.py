from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth


from commerce.errors import error_response

from .models import Admin


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        return admin


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return Admin.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
