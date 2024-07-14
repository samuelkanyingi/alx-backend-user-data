#!/usr/bin/env python3
''' session auth file '''
from flask import jsonify, request, abort, Flask
from api.v1.app import auth  # Import auth locally to avoid circular imports
from models.user import User
import os
from api.v1.views import app_views

''' app = Flask(__name__) '''


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ session login """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    """ Session logout route """
    from api.v1.app import auth  # Importing to avoid circular import issues

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
