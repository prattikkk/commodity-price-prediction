import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from preprocess import load_and_filter
import pandas as pd

series = load_and_filter('ONION', 'BANGALORE')['price']
last_date = series.index[-1]
predict_date = pd.to_datetime('2025-12-01')
days_ahead = (predict_date - last_date).days

print(f'Last date: {last_date}')
print(f'Predict date: {predict_date}')
print(f'Days ahead: {days_ahead}')
