#!/usr/bin/env python3
"""
A basic Flask app
"""
from flask import Flask, abort, jsonify, request, make_response
from flask import Response, redirect
from auth import Auth
from typing import Any


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def home() -> Response:
    """
    Handles GET / requests
    """
    return make_response(jsonify({"message": "Bienvenue"}))


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> Response:
    """
    Register a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(str(email), str(password))
        payload = {"email": user.email, "message": "user created"}
        return make_response(jsonify(payload))
    except ValueError:
        payload = {"message": "email already registered"}
        return make_response(jsonify(payload), 400)


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> Response:
    """
    Handles POST /session requests
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(str(email), str(password)):
        abort(401)

    session_id = AUTH.create_session(str(email))
    res = make_response(jsonify({"email": email, "message": "logged in"}))
    res.set_cookie("session_id", str(session_id))
    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Any:
    """
    Handles DELETE /sessions requests
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(str(session_id))

    if not user:
        abort(403)

    AUTH.destroy_session(int(user.id))
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Response:
    """
    Handles GET /profile requests
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(str(session_id))

    if user:
        return make_response(jsonify({"email": user.email}), 200)

    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> Response:
    """
    Handles POST /reset_password requests
    """
    email = request.form.get("email")

    try:
        token = AUTH.get_reset_password_token(str(email))
    except ValueError:
        abort(403)

    payload = {"email": email, "reset_token": token}
    return make_response(jsonify(payload))


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> Response:
    """
    Handles PUT /reset_password requests
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(str(reset_token), str(new_password))
    except ValueError:
        abort(403)

    payload = {"email": email, "message": "Password updated"}
    return make_response(jsonify(payload))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
