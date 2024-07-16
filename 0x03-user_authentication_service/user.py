#!/usr/bin/env python3
"""
Module defining User model.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        __tablename__ (str): Name of the database table for users.
        id (int): Unique identifier for the user.
        email (str): Email address of the user.
        hashed_password (str): Hashed password of the user.
        session_id (str): Session ID of the user.
        reset_token (str): Token used for password reset.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
