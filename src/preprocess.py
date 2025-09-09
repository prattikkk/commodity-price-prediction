# src/preprocess.py
import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "raw" / "veg_prices.csv"

def load_and_filter(commodity="ONION", district=None):
    df = pd.read_csv(DATA, parse_dates=['date'])
    df = df.rename(columns=str.lower)
    # normalize column names: date, commodity, district, price
    df = df[['date','commodity','district','price']]
    df = df[df['commodity'].str.upper() == commodity.upper()]
    if district:
        df = df[df['district'].str.upper() == district.upper()]
    df = df.sort_values('date').set_index('date').asfreq('D')  # daily frequency
    return df

def make_features(series, nlags=14):
    df = pd.DataFrame({'y': series})
    for lag in range(1, nlags+1):
        df[f'lag_{lag}'] = df['y'].shift(lag)
    df['rolling_7'] = df['y'].rolling(7, min_periods=1).mean().shift(1)
    df = df.dropna()
    return df

if __name__ == "__main__":
    s = load_and_filter(commodity='ONION', district='PUNE')['price']
    Xy = make_features(s)
    print(Xy.tail())
