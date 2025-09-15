#!/usr/bin/env python3
"""
Price Prediction API             if response.status_code == 200:
                result = response.json()
                print("   ✅ Prediction Successful!")
                print(f"   💰 Predicted Price: ₹{result['prediction']:.2f}")
                print(f"   📅 Date: {result['date']}")
            else:
                print(f"   ❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")ipt
This script demonstrates how to use the Indian agricultural price prediction system.
"""

import requests
import json

def test_prediction():
    """Test the price prediction API with sample data."""

    # API endpoint
    url = 'http://localhost:5000/predict'

    # Test cases with different commodities and districts
    test_cases = [
        {
            'commodity': 'ONION',
            'district': 'BANGALORE',
            'date': '2025-06-15',
            'forecast_days': 7
        },
        {
            'commodity': 'POTATO',
            'district': 'MUMBAI',
            'date': '2025-06-20',
            'forecast_days': 7
        },
        {
            'commodity': 'TOMATO',
            'district': 'CHENNAI',
            'date': '2025-06-25',
            'forecast_days': 7
        }
    ]

    print("🌾 Indian Agricultural Price Prediction System")
    print("=" * 50)

    for i, test_data in enumerate(test_cases, 1):
        print(f"\n📊 Test Case {i}:")
        print(f"   Commodity: {test_data['commodity']}")
        print(f"   District: {test_data['district']}")
        print(f"   Date: {test_data['date']}")
        print(f"   Forecast Days: {test_data['forecast_days']}")

        try:
            response = requests.post(url, json=test_data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                print("   ✅ Prediction Successful!")
                print(f"   💰 Predicted Price: ₹{result['prediction']:.2f}")
                print(f"   📅 Date: {result['date']}")
            else:
                print(f"   ❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print("   ❌ Connection Error: Make sure the Flask server is running on localhost:5000")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("🎯 Available Commodities: ONION, POTATO, TOMATO, RICE, WHEAT")
    print("📍 Available Districts: BANGALORE, MUMBAI, CHENNAI, LUCKNOW, KANPUR, etc.")
    print("📅 Date Format: YYYY-MM-DD")
    print("🔮 Forecast Range: 1-30 days")

if __name__ == "__main__":
    test_prediction()
