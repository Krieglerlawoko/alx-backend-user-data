from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class to
    manage the API's auth mechanism."""

    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication
        is required for a given path.
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of
            paths that do not require authentication.

        Returns:
            bool: True if authentication is
            required, False otherwise.
        """
        if path is None or excluded_paths is None:
            return True
        path = path.rstrip('/')
        for ep in excluded_paths:
            if ep.endswith('*'):
                # Check if path matches the pattern before *
                if path.startswith(ep.rstrip('*')):
                    return False
            else:
                # Normalize excluded path by removing trailing slashes
                ep = ep.rstrip('/')
                if path == ep:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the value of the
        Authorization header from the request.
        Args:
            request (Request): The request object.
        Returns:
            str: The value of the Authorization
            header, None if the header is not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method to get the
        current user based on the request.
        This method should be overridden
        in subclasses with actual implementation.
        Args:
            request (Request): The request object.
        Returns:
            TypeVar('User'): The current user,
            None if no user is authenticated.
        """
        return None
