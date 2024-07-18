#!/usr/bin/env python3
"""Flask app module
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """
    GET route that returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def users():
    """
    POST /users route to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"])
def login():
    """ POST  /sessions route """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response

@app.route("/sessions", methods=["DELETE"])
def logout():
    """ DELETE /sessions """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("welcome"))

@app.route("/profile", methods=["GET"])
def profile():
    """ GET /profile """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    # Get the email from the request form data
    email = request.form.get('email')
    
    # Check if the email is provided
    if not email:
        return jsonify({"error": "Email not provided"}), 400
    
    try:
        # Generate reset token
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # If the email is not registered, respond with 403 status code
        abort(403)

    # Respond with the email and reset token
    return jsonify({"email": email, "reset_token": reset_token}), 200

@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ PUT /reset_password """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        return jsonify({"error": "Email, reset token, and new password must be provided"}), 400

    try:
        auth.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
