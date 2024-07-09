from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class to
    manage the API's auth mechanism."""

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
        if not path or not excluded_paths:
            return True

        path_has_trailing_slash = path.endswith('/')
        tmp_path = path if path_has_trailing_slash else path + '/'

        for exc_path in excluded_paths:
            if exc_path.endswith('*'):
                if path.startswith(exc_path[:-1]):
                    return False
            elif path.rstrip('/') == exc_path.rstrip('/'):
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
