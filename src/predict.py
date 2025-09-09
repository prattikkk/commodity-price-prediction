# src/predict.py
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from preprocess import load_and_filter, make_features

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"

def predict_for_date(commodity, district, predict_date, nlags=14):
    # load series
    series = load_and_filter(commodity, district)['price']
    # load models
    arima = joblib.load(MODELS_DIR / f"{district}_arima.pkl")
    scaler = joblib.load(MODELS_DIR / f"{district}_scaler.joblib")
    svr = joblib.load(MODELS_DIR / f"{district}_svm.joblib")

    # ARIMA point forecast for date
    arima_forecast = arima.get_forecast(steps= (pd.to_datetime(predict_date) - series.index[-1]).days )
    arima_mean = arima_forecast.predicted_mean.iloc[-1]

    # build features for SVM: latest lags
    recent = series[-nlags:].values
    if len(recent) < nlags:
        raise ValueError("Not enough data for lags.")
    feat = recent[::-1][:nlags]  # last nlags
    feat_dict = {}
    for i in range(nlags):
        feat_dict[f'lag_{i+1}'] = feat[i]
    feat_df = pd.DataFrame([feat_dict])
    feat_df['rolling_7'] = series[-7:].mean()
    Xs = scaler.transform(feat_df.values)
    residual_pred = svr.predict(Xs)[0]

    final_pred = float(arima_mean + residual_pred)
    return {"district": district, "date": str(predict_date), "prediction": final_pred}

if __name__ == "__main__":
    print(predict_for_date("ONION","PUNE","2025-12-01"))
