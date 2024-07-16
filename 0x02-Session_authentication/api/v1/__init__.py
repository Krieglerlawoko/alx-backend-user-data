#!/usr/bin/env python3
"""
Module for initializing the API blueprint and importing views.
"""

from flask import Blueprint

# Initialize blueprint for API views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all views
from api.v1.views.index import *
from api.v1.views.users import *

# Load user data from file
User.load_from_file()
