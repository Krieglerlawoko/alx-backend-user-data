#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, request, jsonify, abort
from auth import Auth
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=["GET"])
def index():
    """Root endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Endpoint to register a new user"""
    try:
        email = request.form['email']
        password = request.form['password']
        user = auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route("/sessions", methods=["POST"])
def sessions():
    """Endpoint to log in and create a session"""
    try:
        email = request.form['email']
        password = request.form['password']
        if auth.valid_login(email, password):
            session_id = auth.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response, 200
        else:
            abort(401)
    except NoResultFound:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def delete_sessions():
    """Endpoint to log out and delete session"""
    try:
        session_id = request.cookies.get('session_id')
        user = auth.get_user_from_session_id(session_id)
        if user:
            auth.destroy_session(user.id)
            return index()
        else:
            abort(403)
    except NoResultFound:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """Endpoint to retrieve user profile"""
    try:
        session_id = request.cookies.get('session_id')
        user = auth.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    except NoResultFound:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """Endpoint to initiate password reset"""
    try:
        email = request.form['email']
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Endpoint to update password using reset token"""
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        password = request.form['password']
        auth.update_password(reset_token, password)
        return jsonify({"email": email, "message": "password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
