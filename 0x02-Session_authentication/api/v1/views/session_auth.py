#!/usr/bin/env python3
"""
A view that handles all routes for the Session authentication
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    POST /api/v1/auth_session/login

    Return:
      - login to API
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({'error': "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    sid = auth.create_session(users[0].id)
    user = jsonify(users[0].to_json())
    user.set_cookie(os.getenv("SESSION_NAME"), sid)

    return user


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete():
    """
    DELETE /api/v1/auth_session/logout

    Return:
      - logout from API
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200

    abort(404)
