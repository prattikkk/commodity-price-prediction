# src/data_download.py
import os
import requests

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(OUT_DIR, exist_ok=True)

# Fallback: Kaggle-like dataset from GitHub
CSV_URL = "https://raw.githubusercontent.com/akshaybhatia10/Indian-Vegetable-Prices/master/vegetable_prices.csv"
OUT_FILE = os.path.join(OUT_DIR, "veg_prices.csv")

def download_csv(url=CSV_URL, out=OUT_FILE):
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with open(out, 'wb') as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    print("Saved:", out)

if __name__ == "__main__":
    download_csv()
