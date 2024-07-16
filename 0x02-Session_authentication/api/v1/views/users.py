#!/usr/bin/env python3
""" Module for User views """
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
        - List of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
        - User ID
    Return:
        - User object JSON represented
        - 404 if the User ID doesn't exist
    """
    if not user_id:
        abort(404)

    if user_id == "me":
        if not request.current_user:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())

    user = User.get(user_id)
    if not user:
        abort(404)

    if not request.current_user:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
        - User ID
    Return:
        - Empty JSON if the User has been correctly deleted
        - 404 if the User ID doesn't exist
    """
    if not user_id:
        abort(404)

    user = User.get(user_id)
    if not user:
        abort(404)

    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
        - email
        - password
        - last_name (optional)
        - first_name (optional)
    Return:
        - User object JSON represented
        - 400 if can't create the new User
    """
    try:
        rj = request.get_json()
    except Exception:
        return jsonify({'error': 'Wrong format'}), 400

    if not rj or not rj.get("email") or not rj.get("password"):
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        user = User(email=rj.get("email"),
                    password=rj.get("password"),
                    first_name=rj.get("first_name"),
                    last_name=rj.get("last_name"))
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
        - User ID
    JSON body:
        - last_name (optional)
        - first_name (optional)
    Return:
        - User object JSON represented
        - 404 if the User ID doesn't exist
        - 400 if can't update the User
    """
    if not user_id:
        abort(404)

    user = User.get(user_id)
    if not user:
        abort(404)

    rj = request.get_json()
    if not rj:
        return jsonify({'error': 'Wrong format'}), 400

    if 'first_name' in rj:
        user.first_name = rj.get('first_name')
    if 'last_name' in rj:
        user.last_name = rj.get('last_name')

    try:
        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400
