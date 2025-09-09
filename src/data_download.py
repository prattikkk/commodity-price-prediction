# src/data_download.py
import os
import requests

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(OUT, exist_ok=True)

# Replace this with a direct CSV URL from NHB or data.gov.in for a commodity or
# use Kaggle snippet below if using Kaggle dataset
# Example real URL (you may need to find the latest): https://data.gov.in/sites/default/files/vegetable_prices.csv
# For demo, using a placeholder; replace with actual URL
CSV_URL = "https://data.gov.in/sites/default/files/vegetable_prices.csv"  # Placeholder - replace with real URL
OUT_FILE = os.path.join(OUT, "veg_prices.csv")

def download_csv(url=CSV_URL, out=OUT_FILE):
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with open(out, 'wb') as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    print("Saved:", out)

if __name__ == "__main__":
    download_csv()
