#!/usr/bin/env python3
"""
Defines SessionDBAuth class
"""
from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Session Database Authentication
    """

    def create_session(self, user_id=None):
        """
        Creates a session
        """
        sid = super().create_session(user_id)

        if not sid:
            return None

        session = UserSession(user_id=user_id, session_id=sid)
        session.save()

        return sid

    def user_id_for_session_id(self, session_id=None):
        """
        Gets user id for a session
        """
        if not session_id or not type(session_id) is str:
            return None

        sessions = []

        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None

        if not sessions:
            return None

        session = sessions[0]
        exp = session.created_at + timedelta(seconds=self.session_duration)

        if (exp - datetime.now()).total_seconds() < 0:
            session.remove()
            del self.user_id_by_session_id[session_id]
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """
        Destroys a session
        """
        if not request:
            return False

        sid = self.session_cookie(request)

        if not sid:
            return False

        if not self.user_id_for_session_id(sid):
            return False

        session = UserSession.search({"session_id": sid})[0]
        session.remove()

        return True
