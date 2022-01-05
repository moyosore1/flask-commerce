from flask import jsonify


from commerce import db


from .routes import admin
from .auth import basic_auth


@admin.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})
