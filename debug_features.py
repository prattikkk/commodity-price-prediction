import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from preprocess import load_and_filter
import pandas as pd
import numpy as np

print("Loading series...")
series = load_and_filter('ONION', 'BANGALORE')['price']
print(f"Series length: {len(series)}")

nlags = 14
print("Getting recent values...")
recent = series[-nlags:].values
print(f"Recent length: {len(recent)}")

print("Creating feature dict...")
feat_dict = {}
for i in range(nlags):
    feat_dict[f'lag_{i+1}'] = recent[-(i+1)]
print("Feature dict created")

print("Creating DataFrame...")
feat_df = pd.DataFrame([feat_dict])
print("DataFrame created")

print("Adding rolling mean...")
feat_df['rolling_7'] = series[-7:].mean()
print("Feature engineering successful!")
print(f"Feature shape: {feat_df.shape}")
