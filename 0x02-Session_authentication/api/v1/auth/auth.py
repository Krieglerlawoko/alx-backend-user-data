#!/usr/bin/env python3
"""
Class Auth definition.
"""
import os
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Class for managing API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentication.
        
        Args:
            path (str): Url path to be checked.
            excluded_paths (List[str]): List of paths that do not require authentication.
        
        Returns:
            bool: True if path requires authentication, False otherwise.
        """
        if not path:
            return True
        
        if not excluded_paths:
            return True
        
        if path in excluded_paths:
            return False
        
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
            if excluded_path.startswith("/") and path.startswith(excluded_path):
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object.
        
        Args:
            request: Request object.
        
        Returns:
            str: Value of 'Authorization' header, or None if not present.
        """
        if not request:
            return None
        
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on information from a request object.
        
        Args:
            request: Request object.
        
        Returns:
            TypeVar('User'): User instance, or None if not implemented.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the value of a session cookie from a request object.
        
        Args:
            request: Request object.
        
        Returns:
            str: Value of session cookie, or None if not found.
        """
        if not request:
            return None
        
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
