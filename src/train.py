# src/train.py
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from statsmodels.tsa.arima.model import ARIMA
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from preprocess import load_and_filter, make_features

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
MODELS_DIR.mkdir(exist_ok=True, parents=True)

def train_pipeline(commodity, district):
    print(f"Starting training for {commodity} in {district}")
    series = load_and_filter(commodity, district)['price']
    
    # Check if we have enough data points (need at least 30 for reliable training)
    if len(series) < 30:
        raise ValueError(f"Insufficient data: only {len(series)} observations for {commodity} in {district}")
    
    # Keep last 5 days as test split (instead of 30)
    train_series = series.iloc[:-5]
    test_series = series.iloc[-5:]

    # ===== ARIMA (trend) =====
    # Simple auto ARIMA can be replaced by p,d,q grid search. Using small (p,d,q)
    arima_order = (5,1,0)
    arima = ARIMA(train_series, order=arima_order).fit()
    # in-sample fitted values and residuals
    fitted = arima.fittedvalues
    residuals = train_series - fitted

    # ===== Prepare features for SVM on residuals =====
    features = make_features(train_series, nlags=14)
    # target: residuals aligned with features index
    res_series = (train_series - arima.predict(start=train_series.index[0], end=train_series.index[-1])).loc[features.index]
    X = features.drop(columns=['y']).values
    y = res_series.values

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    # simple SVR with small grid
    svr = SVR()
    gs = GridSearchCV(svr, {'C':[1,10], 'gamma':['scale','auto']},
                      cv=TimeSeriesSplit(n_splits=3), scoring='neg_mean_absolute_error', n_jobs=1)
    gs.fit(Xs, y)
    best_svr = gs.best_estimator_

    # save models
    model_prefix = f"{commodity.lower()}_{district.lower()}"
    joblib.dump(scaler, MODELS_DIR / f"{model_prefix}_scaler.joblib")
    joblib.dump(best_svr, MODELS_DIR / f"{model_prefix}_svm.joblib")
    joblib.dump(arima, MODELS_DIR / f"{model_prefix}_arima.pkl")

    print(f"Saved models for {commodity} in {district}")

if __name__ == "__main__":
    # Find all available processed files and extract commodity-district pairs
    processed_dir = Path(__file__).resolve().parents[1] / "data" / "processed"
    available_combinations = []
    
    for file_path in processed_dir.glob("*_processed.csv"):
        filename = file_path.stem  # removes .csv extension
        parts = filename.split("_")
        if len(parts) >= 2:
            commodity = parts[0].upper()
            district = "_".join(parts[1:-1]).upper()  # handle districts with underscores
            available_combinations.append((commodity, district))
    
    print(f"Found {len(available_combinations)} commodity-district combinations to train")
    print("Starting training...")
    
    for commodity, district in available_combinations:
        print(f"Training model for {commodity} in {district}...")
        try:
            # Check data size before training
            series = load_and_filter(commodity, district)['price']
            if len(series) < 30:
                print(f"Skipping {commodity} in {district}: insufficient data ({len(series)} observations)")
                continue
                
            train_pipeline(commodity, district)
            print(f"Successfully trained {commodity} in {district}")
        except Exception as e:
            print(f"Failed to train {commodity} in {district}: {e}")
    print("Training completed.")
