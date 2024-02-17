#!/usr/bin/env python3
"""
Defines Session Expiration
"""
from .session_auth import SessionAuth
from flask import request
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session Expiration class
    """
    def __init__(self):
        """
        The constructor.
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session ID
        """
        sid = super().create_session(user_id)

        if not sid:
            return None

        self.user_id_by_session_id[sid] = {
                "user_id": user_id,
                "created_at": datetime.now()
                }

        return sid

    def user_id_for_session_id(self, session_id=None):
        """
        Get user id from session
        """
        if not session_id:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        session = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session.get("user_id")

        if not session.get("created_at"):
            return None

        created_at = session.get("created_at")
        exp = created_at + timedelta(seconds=self.session_duration)

        if (exp - datetime.now()).total_seconds() < 0:
            return None

        return session.get("user_id")
