#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.predict import predict_for_date

# Test the prediction function directly
print("Testing prediction function directly...")
try:
    result = predict_for_date('ONION', 'BANGALORE', '2024-01-15', 7)
    print("SUCCESS!")
    print(f"Result: {result}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
