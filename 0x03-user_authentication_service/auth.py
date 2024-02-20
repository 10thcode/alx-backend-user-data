#!/usr/bin/env python3
"""
Defines _hash_password method
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Create a salted hash
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def _generate_uuid() -> str:
    """
    This method generates a uuid and returns it.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """
        The constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Save a user to the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
        else:
            raise ValueError("User {} already exists".format(email))

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check for valid login
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> Union[str | None]:
        """
        Generate a new UUID and store it in the database
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(int(user.id), session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User | None]:
        """
        Get a user
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a new UUID and update the user’s
        reset_token database field.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        token = _generate_uuid()
        self._db.update_user(int(user.id), reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update user's hashed password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_pwd = _hash_password(password)
        self._db.update_user(int(user.id),
                             hashed_password=hashed_pwd,
                             reset_token=None)
