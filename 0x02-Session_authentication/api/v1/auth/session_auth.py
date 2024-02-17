#!/usr/bin/env python3
"""
Defines SessionAuth class
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session
        """
        if user_id is None:
            return None

        if not type(user_id) is str:
            return None

        sid = uuid.uuid4()
        self.user_id_by_session_id[sid] = user_id

        return sid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Gets a User ID
        """
        if session_id is None:
            return None

        if not type(session_id) is str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Gets user instance
        """
        sid = self.session_cookie(request)
        uid = self.user_id_for_session_id(sid)

        return (User.get(uid))
