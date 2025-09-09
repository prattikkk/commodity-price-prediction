# AI-ML Price Predictor MVP

This is a Flask-based web application that predicts commodity prices using a hybrid ARIMA + SVM model.

## Features

- Hybrid forecasting model combining ARIMA for trend and SVM for residual correction
- REST API for price predictions
- Supports multiple districts and commodities
- Simple evaluation metrics

## Setup

1. Place dataset CSV in `data/raw/veg_prices.csv` (or run `python src/data_download.py`).
2. Install dependencies: `pip install -r requirements.txt`
3. Preprocess & inspect: `python src/preprocess.py`
4. Train (example for PUNE): `python src/train.py`
5. Run server: `python src/app.py`
6. Test: `curl -X POST http://localhost:5000/predict -H "Content-Type:application/json" -d '{"commodity":"ONION","district":"PUNE","date":"2025-12-01"}'`

## API Usage

POST /predict

Request body:
```json
{
  "commodity": "ONION",
  "district": "PUNE",
  "date": "2025-12-01"
}
```

Response:
```json
{
  "district": "PUNE",
  "date": "2025-12-01",
  "prediction": 45.67
}
```

## Project Structure

```
price-predictor/
├── data/
│   └── raw/                # Downloaded CSV(s)
├── src/
│   ├── data_download.py
│   ├── preprocess.py
│   ├── train.py
│   ├── predict.py
│   └── app.py
├── models/
│   └── <district>_arima.pkl
│   └── <district>_svm.joblib
├── requirements.txt
└── README.md
```
