# src/preprocess.py
import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "raw" / "kaggle_Agriculture_price_dataset.csv"

def load_and_filter(commodity="ONION", district=None):
    df = pd.read_csv(DATA)
    # normalize column names to match our expected format
    df = df.rename(columns={
        'STATE': 'state',
        'District Name': 'district', 
        'Commodity': 'commodity',
        'Modal_Price': 'price',
        'Price Date': 'date'
    })
    df = df[['date','commodity','district','price']]
    df = df[df['commodity'].str.upper() == commodity.upper()]
    if district:
        df = df[df['district'].str.upper() == district.upper()]
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    # Handle duplicates by taking mean price for same date
    df = df.groupby('date')['price'].mean().reset_index()
    df = df.sort_values('date').set_index('date').asfreq('D')  # daily frequency
    df = df.dropna()
    return df

def make_features(series, nlags=14):
    df = pd.DataFrame({'y': series})
    for lag in range(1, nlags+1):
        df[f'lag_{lag}'] = df['y'].shift(lag)
    df['rolling_7'] = df['y'].rolling(7, min_periods=1).mean().shift(1)
    df = df.dropna()
    return df

if __name__ == "__main__":
    df = pd.read_csv(DATA, encoding='utf-8-sig')
    # normalize column names to match our expected format
    df = df.rename(columns={
        'STATE': 'state',
        'District Name': 'district', 
        'Commodity': 'commodity',
        'Modal_Price': 'price',
        'Price Date': 'date'
    })
    print("Columns:", df.columns.tolist())
    print("Unique commodities:", df['commodity'].unique()[:10])  # first 10
    print("Unique districts:", df['district'].unique()[:10])  # first 10
    print("Data shape:", df.shape)
    print("First 5 rows:")
    print(df.head())
    
    # Process data for each district
    processed_dir = Path(__file__).resolve().parents[1] / "data" / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    for commodity in df['commodity'].unique():
        for district in df[df['commodity'].str.upper() == commodity.upper()]['district'].unique():
            print(f"Processing {commodity} in {district}...")
            s = load_and_filter(commodity=commodity, district=district)['price']
            if len(s) > 14:  # need at least 14 days for features
                Xy = make_features(s)
                output_file = processed_dir / f"{commodity.lower()}_{district.lower()}_processed.csv"
                Xy.to_csv(output_file)
                print(f"Saved {len(Xy)} rows to {output_file}")
            else:
                print(f"Not enough data for {commodity} in {district}")
