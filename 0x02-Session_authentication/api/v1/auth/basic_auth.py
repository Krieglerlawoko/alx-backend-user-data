#!/usr/bin/env python3
"""
Class BasicAuth definition.
"""
import base64
from typing import TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Implementation of Basic Authorization protocol methods.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header.
        """
        if not isinstance(authorization_header, str) or not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[-1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64-encoded string.
        """
        try:
            decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from a decoded Base64 string.
        """
        if not isinstance(decoded_base64_authorization_header, str) or ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(":", 1)
        return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password credentials.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if users:
                for user in users:
                    if user.is_valid_password(user_pwd):
                        return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves a User instance based on the request's authorization credentials.
        """
        if not request:
            return None

        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                decoded = self.decode_base64_authorization_header(token)
                if decoded:
                    email, password = self.extract_user_credentials(decoded)
                    if email:
                        return self.user_object_from_credentials(email, password)
        return None
