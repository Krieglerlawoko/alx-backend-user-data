#!/usr/bin/env python3
"""
User module
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User class"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self):
    return (f"<User(id={self.id}, email='{self.email}', "
            f"hashed_password='{self.hashed_password[:10]}...', "
            f"session_id='{self.session_id}', "
            f"reset_token='{self.reset_token}')>")
