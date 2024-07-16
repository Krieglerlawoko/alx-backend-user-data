#!/usr/bin/env python3
"""
Module for Session authentication with expiration
and storage support of the API.
"""
from datetime import datetime, timedelta
from typing import Optional

from flask import request
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Session authentication class with expiration and database storage support.
    """

    def create_session(self, user_id: str) -> Optional[str]:
        """
        Creates and stores a session ID for the given user ID.
        Args:
            user_id (str): User ID.
        Returns:
            Optional[str]
        """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str) -> Optional[str]:
        """
        Retrieves the user ID associated with a given session ID,
        verifying session expiration.
        Args:
            session_id (str): Session ID.
        Returns:
            Optional[str]: User ID, or None if session is invalid or expired.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if not sessions:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroys an authenticated session.
        Args:
            request: Request object containing session cookie.
        Returns:
            bool: True if session was successfully destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if not sessions:
            return False
        sessions[0].remove()
        return True
