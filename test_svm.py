import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from preprocess import load_and_filter
import pandas as pd
import numpy as np
import joblib

print("Loading series...")
series = load_and_filter('ONION', 'BANGALORE')['price']

nlags = 14
recent = series[-nlags:].values
feat_dict = {}
for i in range(nlags):
    feat_dict[f'lag_{i+1}'] = recent[-(i+1)]
feat_df = pd.DataFrame([feat_dict])
feat_df['rolling_7'] = series[-7:].mean()

print("Loading scaler...")
scaler = joblib.load('models/onion_bangalore_scaler.joblib')
print("Scaler loaded")

print("Transforming features...")
Xs = scaler.transform(feat_df.values)
print("Scaler transform successful")

print("Loading SVM...")
svr = joblib.load('models/onion_bangalore_svm.joblib')
print("SVM loaded")

print("Making prediction...")
pred = svr.predict(Xs)
print(f"SVM prediction: {pred[0]}")

print("All components working!")
