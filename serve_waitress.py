#!/usr/bin/env python3
"""Serve the app using Waitress (Windows-friendly WSGI server)."""
from waitress import serve
from src.app import app

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)
