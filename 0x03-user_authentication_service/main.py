#!/usr/bin/env python3
"""
Module for end-to-end (E2E) integration tests for `app.py`.
"""

import requests
from app import AUTH

BASE_URL = "http://0.0.0.0:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test the registration of a user."""
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}

    # Attempt to register a new user
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    # Attempt to register the same user again
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test logging in with wrong password."""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}

    # Attempt to log in with incorrect password
    response = requests.post(url, data=data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Test retrieving profile information while being logged out."""
    url = f"{BASE_URL}/profile"

    # Attempt to retrieve profile information without session ID
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test retrieving profile information while logged in."""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}

    # Retrieve profile information with valid session ID
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200

    # Validate the returned email matches the logged-in user's email
    payload = response.json()
    user = AUTH.get_user_from_session_id(session_id)
    assert "email" in payload
    assert payload["email"] == user.email


def log_out(session_id: str) -> None:
    """Test logging out from a session."""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}

    # Attempt to log out with valid session ID
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Test requesting a password reset."""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}

    # Request a password reset
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email

    # Return the reset token for further testing
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating a user's password."""
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    # Update the user's password using the reset token
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated"
    assert response.json()["email"] == email


def log_in(email: str, password: str) -> str:
    """Test logging in."""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}

    # Attempt to log in with valid credentials
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert "message" in response.json()
    assert response.json()["email"] == email

    # Return the session ID from the response cookie
    return response.cookies.get("session_id")


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
