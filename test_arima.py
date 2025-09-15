import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from preprocess import load_and_filter
import joblib

series = load_and_filter('ONION', 'BANGALORE')['price']
arima = joblib.load('models/onion_bangalore_arima.pkl')

print('Testing ARIMA forecast for 9 steps...')
forecast = arima.get_forecast(steps=9)
print('ARIMA forecast successful')
print('Predicted mean:', forecast.predicted_mean.iloc[-1])
