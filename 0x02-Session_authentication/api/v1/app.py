#!/usr/bin/env python3
"""
Route module for the API.
"""

import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Authentication setup
AUTH_TYPE = os.getenv("AUTH_TYPE")

auth = None
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def authenticate_user() -> None:
    """
    Authenticates a user before processing a request.
    """
    if auth:
        request.current_user = auth.current_user(request)
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if auth.require_auth(request.path, excluded_paths):
            auth_header = auth.authorization_header(request)
            session_cookie = auth.session_cookie(request)
            current_user = auth.current_user(request)

            if not auth_header and not session_cookie:
                abort(401, description="Unauthorized")
 
            if not current_user:
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles Not Found error.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles Unauthorized error.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles Forbidden error.
    """
    return jsonify({"error": "Forbidden"}), 403


def run_app() -> None:
    """
    Run the Flask app with the specified host and port.
    """
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "5000"))
    app.run(host=host, port=port)


if __name__ == "__main__":
    run_app(host=host, port=port)
