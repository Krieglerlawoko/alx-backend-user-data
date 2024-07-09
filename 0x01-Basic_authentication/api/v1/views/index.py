#!/usr/bin/env python3
"""
Module defining the routes and views for the API
"""

from flask import Flask, jsonify, abort, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/v1/status/', methods=['GET'])
def status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"}), 200


@app.route('/api/v1/unauthorized/', methods=['GET'])
def unauthorized():
    """ Unauthorized access route for testing """
    abort(401)


@app.route('/api/v1/forbidden/', methods=['GET'])
def forbidden():
    """ Forbidden access route for testing """
    abort(403)


@app.route('/api/v1/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    """
    A catch-all route to handle undefined routes and methods.
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def before_request():
    """ Handle request filtering based on authentication """
    auth = None  # Placeholder for auth
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
