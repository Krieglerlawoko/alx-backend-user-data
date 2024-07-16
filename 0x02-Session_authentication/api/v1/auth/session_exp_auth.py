#!/usr/bin/env python3
"""
SessionExpAuth class definition with session expiration.
"""
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Session authentication class with session expiration support.
    """

    def __init__(self):
        """
        Initializes the SessionExpAuth class
        """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str) -> str:
        """
        Creates a session ID
        Args:
            user_id (str): User ID.
        Returns:
            str: Session ID, or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id:
            session_details = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            self.user_id_by_session_id[session_id] = session_details
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str) -> str:
        """
        Args:
            session_id (str): Session ID.
        Returns:
            str: User ID, or None if session is invalid or expired.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        session_details = self.user_id_by_session_id.get(session_id)
        if session_details is None or "created_at" not in session_details:
            return None
        created_at = session_details["created_at"]
        if self.session_duration > 0:
            expiration_time = (created_at +
                               timedelta(seconds=self.session_duration))
            if expiration_time < datetime.now():
                return None
        return session_details.get("user_id")
