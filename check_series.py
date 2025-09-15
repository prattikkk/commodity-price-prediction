import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from preprocess import load_and_filter

series = load_and_filter('ONION', 'BANGALORE')['price']
print('Last 20 dates:')
print(series.index[-20:])
print('Last 20 values:')
print(series.values[-20:])
print(f'Series length: {len(series)}')
print(f'Last 14 values: {series.values[-14:]}')
print(f'Length of last 14: {len(series.values[-14:])}')
