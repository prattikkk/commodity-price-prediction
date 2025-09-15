#!/usr/bin/env python3
"""UI smoke test: POST form data to /predict-ui and ensure result page renders a prediction or clear error.
"""
from pathlib import Path
import sys

# Ensure src on path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))
from app import app

sample = {
    'commodity': 'ONION',
    'district': 'BANGALORE',
    'date': '2025-06-15',
    'forecast_days': '7',
}

if __name__ == '__main__':
    app.testing = True
    client = app.test_client()

    # GET index should be 200
    r = client.get('/')
    print('GET / status', r.status_code)

    # POST /predict-ui with form data
    resp = client.post('/predict-ui', data=sample)
    text = resp.get_data(as_text=True)
    print('POST /predict-ui status', resp.status_code)
    print('Has error?', 'Missing required fields' in text)
    print('Has prediction?', 'Predicted Price:' in text)
