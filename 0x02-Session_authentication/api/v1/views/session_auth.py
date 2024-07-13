#!/usr/bin/env python3
''' session auth file '''
from flask import jsonify, request, abort, Flask
from api.v1.app import auth  # Import auth locally to avoid circular imports
from models.user import User
import os


app = Flask(__name__)


@app.route('/api/v1/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
