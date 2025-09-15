import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from preprocess import load_and_filter

print('Calling load_and_filter...')
series = load_and_filter('ONION', 'BANGALORE')
print('Series loaded successfully, length:', len(series))
print('First few dates:', series.index[:5])
print('Last few dates:', series.index[-5:])
