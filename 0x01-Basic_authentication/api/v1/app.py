#!/usr/bin/env python3
"""
API module
"""
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """ Handle request filtering based on authentication """
    if auth is None:
        return
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error):
    """ Handle unauthorized request error """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Handle forbidden request error """
    return jsonify({"error": "Forbidden"}), 403


@app.route('/api/v1/status', methods=['GET'])
def status():
    """ Return the status of the API """
    return jsonify({"status": "OK"})


@app.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized_route():
    """ Endpoint to raise a 401 error for testing """
    abort(401)


@app.route('/api/v1/forbidden', methods=['GET'])
def forbidden_route():
    """ Endpoint to raise a 403 error for testing """
    abort(403)


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    app.run(host=host, port=port)
