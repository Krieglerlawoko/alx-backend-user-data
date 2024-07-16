#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine authentication type
AUTH_TYPE = os.getenv("AUTH_TYPE")
auth = None
if AUTH_TYPE == "auth":
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Filter each request before it's handled by the proper route
    """
    if auth and auth.require_auth(request.path, [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]):
        cookie = auth.session_cookie(request)
        if auth.authorization_header(request) is None and cookie is None:
            abort(401, description="Unauthorized")
        if auth.current_user(request) is None:
            abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error):
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """ Request unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Request unauthorized handler """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
