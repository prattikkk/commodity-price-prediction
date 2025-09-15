import requests
import time

# Test the prediction API
url = 'http://localhost:5000/predict'
data = {
    'commodity': 'ONION',
    'district': 'BANGALORE',
    'date': '2024-01-15',
    'forecast_days': 7
}

print("Testing API connection...")
print(f"URL: {url}")
print(f"Data: {data}")

# Wait a moment for server to be ready
time.sleep(2)

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error Response: {response.text}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
    print("Make sure the Flask server is running on localhost:5000")
except Exception as e:
    print(f"Error: {e}")
