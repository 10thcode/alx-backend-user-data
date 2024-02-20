#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Any, Optional

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session: Optional[Session] = None

    @property
    def _session(self) -> Any:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Saves the user to the database.
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs: Any) -> User:
        """
        Gets the first row found in the users table
        """
        session = self._session
        query = session.query(User)
        for k, v in kwargs.items():
            try:
                query = query.filter(getattr(User, k) == v)
            except AttributeError:
                raise InvalidRequestError

        return query.one()

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """
        Update user attributes
        """
        user = self.find_user_by(id=user_id)
        session = self._session
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError

        session.commit()
