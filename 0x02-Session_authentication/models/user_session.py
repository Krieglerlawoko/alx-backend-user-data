#!/usr/bin/env python3
"""Module User session.
"""
from models.base import Base


class UserSession(Base):
    """User session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """User session instance initialized.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
