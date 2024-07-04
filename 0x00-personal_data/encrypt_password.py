#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password: Plain text password.

    Returns:
        Salted, hashed password as bytes.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if a password matches its hashed version.

    Args:
        hashed_password: Hashed password as bytes.
        password: Plain text password.

    Returns:
        True if passwords match, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
