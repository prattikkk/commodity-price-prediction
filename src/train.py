# src/train.py
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from statsmodels.tsa.arima.model import ARIMA
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from preprocess import load_and_filter, make_features

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
MODELS_DIR.mkdir(exist_ok=True, parents=True)

def train_pipeline(commodity, district):
    series = load_and_filter(commodity, district)['price']
    # Keep last 30 days as test split
    train_series = series.iloc[:-30]
    test_series = series.iloc[-30:]

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
    joblib.dump(scaler, MODELS_DIR / f"{district}_scaler.joblib")
    joblib.dump(best_svr, MODELS_DIR / f"{district}_svm.joblib")
    joblib.dump(arima, MODELS_DIR / f"{district}_arima.pkl")

    print("Saved models for", district)

if __name__ == "__main__":
    train_pipeline("ONION", "PUNE")
