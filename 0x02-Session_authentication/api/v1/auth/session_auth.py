#!/usr/bin/env python3
"""
Class SessionAuth definition.
"""
import base64
from uuid import uuid4
from typing import Optional

from .auth import Auth  # Assuming this is the relative path to your Auth class
from models.user import User


class SessionAuth(Auth):
    """
    Implementation of Session Authorization protocol methods.
    """

    def __init__(self):
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str) -> Optional[str]:
        """
        Creates a session ID for a user with the given user ID.
        Args:
            user_id (str): User's ID.
        Returns:
            Optional[str]
        """
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str) -> Optional[str]:
        """
        Retrieves the user ID associated with a session ID.
        Args:
            session_id (str): Session ID.
        Returns:
            Optional[str]: User ID, or None if session_id is invalid.
        """
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Optional[User]:
        """
        Retrieves the current user based on the session ID
        Args:
            request: Request object containing the session cookie.
        Returns:
            Optional[User]: User instance
        """
        if request is None:
            return None
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return None
        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the session associated with the request.
        Args:
            request: Request object containing the session cookie.
        Returns:
            bool: True if session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False
        if session_cookie in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_cookie]
            return True
        return False
