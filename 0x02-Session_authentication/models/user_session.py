#!/usr/bin/env python3
"""
Defines UserSession class
"""
from models.base import Base


class UserSession(Base):
    """
    User session
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        The constructor
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
