#!/usr/bin/env python3
"""
Indian Agricultural Price Prediction System - Direct Test
This script demonstrates the core prediction functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from predict import predict_for_date

def main():
    print("🌾 Indian Agricultural Price Prediction System")
    print("=" * 60)
    print("Using real mandi price data from Kaggle dataset")
    print("=" * 60)

    # Test cases
    test_cases = [
        ("ONION", "BANGALORE", "2025-06-15"),
        ("POTATO", "MUMBAI", "2025-06-20"),
        ("TOMATO", "CHENNAI", "2025-06-25"),
        ("RICE", "LUCKNOW", "2025-06-30"),
        ("WHEAT", "KANPUR", "2025-07-05")
    ]

    print("\n📊 Running Predictions:\n")

    for commodity, district, date in test_cases:
        print(f"🔍 Predicting {commodity} price in {district} for {date}")
        try:
            result = predict_for_date(commodity, district, date, 7)
            print(f"   💰 Predicted Price: ₹{result['prediction']:.2f}")
            print(f"   📅 Date: {result['date']}")
            print("   ✅ Success!\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")

    print("=" * 60)
    print("🎯 System Features:")
    print("   • Real Indian mandi price data (2023-2025)")
    print("   • ARIMA + SVM hybrid forecasting")
    print("   • Multiple commodities: ONION, POTATO, TOMATO, RICE, WHEAT")
    print("   • Multiple districts across India")
    print("   • 7-day forecast horizon")
    print("\n🚀 Flask API running on: http://localhost:5000/predict")
    print("   POST request format:")
    print("   {")
    print('     "commodity": "ONION",')
    print('     "district": "BANGALORE",')
    print('     "date": "2025-06-15",')
    print('     "forecast_days": 7')
    print("   }")
    print("=" * 60)

if __name__ == "__main__":
    main()
