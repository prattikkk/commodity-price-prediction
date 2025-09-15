#!/usr/bin/env python3
"""
Local API smoke test using Flask's test client (no network/ports required).
"""
from pathlib import Path
import sys

# Ensure src on path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))
from app import app

samples = [
    {"commodity": "ONION", "district": "BANGALORE", "date": "2025-06-15"},
    {"commodity": "POTATO", "district": "MUMBAI", "date": "2025-06-20"},
]

if __name__ == '__main__':
    app.testing = True
    client = app.test_client()

    print("Health:", client.get('/health').json)
    for s in samples:
        print("Request:", s)
        resp = client.post('/predict', json=s)
        print("Status:", resp.status_code)
        print("Body:", resp.json)
        print("-")
