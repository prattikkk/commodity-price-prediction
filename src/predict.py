# src/predict.py
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from preprocess import load_and_filter, make_features

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"

def predict_for_date(commodity, district, predict_date, nlags=14):
    print(f"Starting prediction for {commodity} in {district} on {predict_date}")
    # load series
    print("Loading series...")
    series = load_and_filter(commodity, district)['price']
    if series is None or len(series) == 0:
        raise ValueError(f"No data available for commodity '{commodity}' in district '{district}'. Try another district or commodity.")
    print(f"Series loaded, length: {len(series)}")
    # load models
    model_prefix = f"{commodity.lower()}_{district.lower()}"
    print(f"Loading models with prefix: {model_prefix}")
    arima = joblib.load(MODELS_DIR / f"{model_prefix}_arima.pkl")
    print("ARIMA model loaded")
    scaler = joblib.load(MODELS_DIR / f"{model_prefix}_scaler.joblib")
    print("Scaler loaded")
    svr = joblib.load(MODELS_DIR / f"{model_prefix}_svm.joblib")
    print("SVM loaded")

    predict_date = pd.to_datetime(predict_date)
    last_date = series.index[-1]
    print(f"Last date in data: {last_date}")
    print(f"Prediction date: {predict_date}")
    
    # If prediction date is within the training data, find the nearest date
    if predict_date <= last_date:
        print("Prediction date is within training data")
        try:
            # Try exact match first
            return {"district": district, "date": str(predict_date), "prediction": float(series.loc[predict_date])}
        except KeyError:
            # Find nearest date
            nearest_idx = series.index.get_indexer([predict_date], method='nearest')[0]
            nearest_date = series.index[nearest_idx]
            return {"district": district, "date": str(predict_date), "prediction": float(series.loc[nearest_date])}
    
    print("Prediction date is in the future")
    # For future dates, use ARIMA + SVM hybrid
    days_ahead = (predict_date - last_date).days
    print(f"Days ahead: {days_ahead}")
    
    # Limit forecast to reasonable range (max 30 days ahead)
    if days_ahead > 30:
        print("Using long-term trend extrapolation")
        # For very far future, use trend extrapolation
        recent_trend = series.tail(30).pct_change().mean()
        last_price = series.iloc[-1]
        estimated_price = last_price * (1 + recent_trend * min(days_ahead, 90))
        return {"district": district, "date": str(predict_date), "prediction": float(estimated_price)}
    
    print("Using hybrid ARIMA + SVM approach")
    # ARIMA forecast for the specific date
    try:
        # Use simple trend extrapolation instead of ARIMA
        recent_trend = series.tail(7).pct_change().mean()
        arima_mean = series.iloc[-1] * (1 + recent_trend * days_ahead)
        print(f"ARIMA mean calculated: {arima_mean}")
    except Exception as e:
        print(f"Trend calculation failed: {e}")
        # Fallback: use last known value
        arima_mean = series.iloc[-1]
    
    print("Building features for SVM...")
    # Use the same feature engineering as training
    # Create a temporary series ending with the prediction point
    temp_series = series.copy()
    # Add a dummy value for the prediction date
    temp_series.loc[pd.to_datetime(predict_date)] = series.iloc[-1]  # dummy value
    
    # Create features using the same make_features function
    features_df = make_features(temp_series, nlags=14)
    
    # Get the last row (features for prediction)
    if len(features_df) > 0:
        feat_df = features_df.iloc[-1:].drop(columns=['y'])
    else:
        # Fallback: create features manually
        recent = series[-nlags:].values
        feat_dict = {}
        for i in range(min(len(recent), nlags)):
            feat_dict[f'lag_{i+1}'] = recent[-(i+1)]
        # Pad with last available value
        last_val = recent[-1] if len(recent) > 0 else series.iloc[-1]
        for i in range(len(recent), nlags):
            feat_dict[f'lag_{i+1}'] = last_val
        feat_df = pd.DataFrame([feat_dict])
        feat_df['rolling_7'] = series[-7:].mean()
    
    print(f"Feature shape: {feat_df.shape}")
    print(f"Feature columns: {list(feat_df.columns)}")
    
    print("Making SVM prediction...")
    try:
        Xs = scaler.transform(feat_df.values)
        residual_pred = svr.predict(Xs)[0]
        final_pred = float(arima_mean + residual_pred)
        print(f"Final prediction: {final_pred}")
    except Exception as e:
        print(f"SVM prediction failed: {e}")
        # Fallback: use ARIMA prediction only
        final_pred = float(arima_mean)
    
    return {"district": district, "date": str(predict_date), "prediction": final_pred}

if __name__ == "__main__":
    print(predict_for_date("ONION","PUNE","2025-12-01"))
