#!/usr/bin/env python3
"""
Defines BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Gets the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None

        if type(authorization_header) is not str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self, b: str) -> str:
        """
        Gets the decoded value of a Base64 string
        base64_authorization_header
        """
        if b is None:
            return None

        if type(b) is not str:
            return None

        try:
            return base64.b64decode(b).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, d: str) -> (str, str):
        """
        Gets the user email and password from the Base64 decoded value.
        """
        if d is None:
            return (None, None)

        if type(d) is not str:
            return (None, None)

        if ":" not in d:
            return (None, None)

        return tuple(d.split(":"))
