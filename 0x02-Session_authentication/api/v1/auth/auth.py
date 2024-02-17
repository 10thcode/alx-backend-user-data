#!/usr/bin/env python3
"""
Defines Auth class
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """
    Manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if path is excluded
        """
        if path and excluded_paths:
            path = path + '/' if not path.endswith('/') else path
            if path in excluded_paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None
        """
        if request is None:
            return None

        if not request.headers.get("Authorization"):
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None

    def session_cookie(self, request=None):
        """
        Gets cookie value from a request
        """
        if request is None:
            return None

        sid = os.getenv("SESSION_NAME")
        return request.cookies.get(sid)
