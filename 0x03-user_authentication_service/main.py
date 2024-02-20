#!/usr/bin/env python3
"""
Main file
"""
import requests
import json


URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Query POST /users endpoint
    """
    url = "{}/users".format(URL)
    payload = {"email": email, "password": password}
    res = requests.post(url, data=payload)
    assert res.json() == {"email": EMAIL, "message": "user created"}
    assert res.status_code == 200
    res = requests.post(url, data=payload)
    assert res.json() == {"message": "email already registered"}
    assert res.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Query /sessions endpoint
    """
    url = "{}/sessions".format(URL)
    payload = {"email": email, "password": password}
    res = requests.post(url, data=payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Query /sessions endpoint
    """
    url = "{}/sessions".format(URL)
    payload = {"email": email, "password": password}
    res = requests.post(url, data=payload)
    assert res.json() == {"email": EMAIL, "message": "logged in"}
    assert res.status_code == 200
    assert "session_id" in res.cookies
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Query GET /profile endpoint
    """
    url = "{}/profile".format(URL)
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Query /profile endpoint
    """
    url = "{}/profile".format(URL)
    res = requests.get(url, cookies={"session_id": session_id})
    assert res.json() == {"email": EMAIL}
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """
    Query DELETE /sessions endpoint
    """
    url = "{}/sessions".format(URL)
    res = requests.delete(url, cookies={"session_id": session_id})
    assert res.history and res.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Query /reset_password endpoint
    """
    url = "{}/reset_password".format(URL)
    res = requests.post(url, data={"email": email})
    assert "reset_token" in res.json()
    reset_token = res.json().get("reset_token")
    assert res.json() == {"email": EMAIL, "reset_token": reset_token}
    assert res.status_code == 200
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Query PUT /reset_password endpoint
    """
    url = "{}/reset_password".format(URL)
    payload = {"email": email,
               "reset_token": reset_token,
               "new_password": new_password}
    res = requests.put(url, data=payload)
    assert res.json() == {"email": EMAIL, "message": "Password updated"}
    assert res.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
