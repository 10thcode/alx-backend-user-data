#!/usr/bin/env python3
"""
Defines Auth class
"""
from flask import request
from typing import List, TypeVar


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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
