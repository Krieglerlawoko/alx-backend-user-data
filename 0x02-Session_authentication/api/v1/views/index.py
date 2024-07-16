#!/usr/bin/env python3
"""
Module for Index views.
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status

    Return:
        JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', methods=['GET'], strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats

    Return:
        JSON response containing the count of each object type.
    """
    from models.user import User

    stats = {
        'users': User.count()
    }
    return jsonify(stats)


@app_views.route('/unauthorized/', methods=['GET'], strict_slashes=False)
def unauthorized() -> None:
    """
    GET /api/v1/unauthorized

    Return:
        Aborts the request with a 401 Unauthorized error.
    """
    abort(401)


@app_views.route('/forbidden/', methods=['GET'], strict_slashes=False)
def forbidden() -> None:
    """
    GET /api/v1/forbidden

    Return:
        Aborts the request with a 403 Forbidden error.
    """
    abort(403)
