#!/usr/bin/env python3
"""
Defines BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


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

        return d[:d.index(':')], d[d.index(':') + 1:]

    def user_object_from_credentials(self, email: str,
                                     pwd: str) -> TypeVar('User'):
        """
        Gets the User instance based on his email and password.
        """
        if email is None or type(email) is not str:
            return None

        if pwd is None or type(pwd) is not str:
            return None

        user = User.search({"email": email})
        if user and user[0].is_valid_password(pwd):
            return user[0]

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User instance
        for a request
        """
        auth = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(auth)
        db64 = self.decode_base64_authorization_header(b64)
        details = self.extract_user_credentials(db64)
        email = details[0]
        pwd = details[1]
        user = self.user_object_from_credentials(email, pwd)

        return user
