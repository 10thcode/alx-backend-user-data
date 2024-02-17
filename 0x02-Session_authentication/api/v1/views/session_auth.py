#!/usr/bin/env python3
"""
A view that handles all routes for the Session authentication
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    GET /api/v1/auth_session/login

    Return:
      - the status of the API
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({'error': "email missing"}, 400)

    if not password:
        return jsonify({"error": "password missing"}, 400)

    users = User.search({"email", email})

    if not users:
        return jsonify({"error": "no user found for this email"}, 404)

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}, 401)

    from api.v1.app import auth

    sid = auth.create_session(user.id)
    user = jsonify(user.to_json())
    user.set_cookie(getenv("SESSION_NAME"), new_session_id)

    return user
