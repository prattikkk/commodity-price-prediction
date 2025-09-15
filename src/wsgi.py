"""WSGI entrypoint for production servers.
Exports `application` for WSGI runners.
"""
from app import app as application  # noqa: F401
