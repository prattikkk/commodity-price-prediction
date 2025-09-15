# src/data_download_agmarknet.py
import requests
import pandas as pd
import os

API_KEY = "579b464db66ec23bdd0000010e91db6437e04e8b41cbb9c6b264a921"
RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
LIMIT = 5000   # max records per request (default is 100, can go up to 5000)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_FILE = os.path.join(OUT_DIR, "agmarknet_prices.csv")

def download_agmarknet():
    url = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24?api-key=579b464db66ec23bdd00000151df0357a4d5466f6bd2b74a97ef2213&format=csv"
    print("Fetching:", url)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    
    # Save the CSV content directly
    with open(OUT_FILE, 'wb') as f:
        f.write(r.content)
    
    print(f"Downloaded data to {OUT_FILE}")
    
    # Load and show basic info
    df = pd.read_csv(OUT_FILE)
    print(f"Loaded {len(df)} records")
    print("Columns:", df.columns.tolist())
    print("First 5 rows:")
    print(df.head())

if __name__ == "__main__":
    download_agmarknet()
