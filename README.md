# Price Predictor

Simple Flask app that predicts Indian agri commodity prices using a hybrid ARIMA + SVM model. Includes a web UI and JSON API.

## Features
- Web UI with commodity/district dropdowns and date selection
- JSON API for programmatic access
- Production-friendly (Waitress on Windows)
- Dockerfile and basic CI workflow

## Quickstart (Local)
1. Python 3.11
2. Install dependencies
   - python -m pip install --upgrade pip
   - pip install -r requirements.txt
3. Run
   - Dev: python src/app.py
   - Production-like: python serve_waitress.py
4. Open http://127.0.0.1:5000

## Web UI
- Choose a commodity; districts list filters automatically.
- Pick a date (defaults to today) and click Predict Price.

## JSON API
POST /predict

Headers: Content-Type: application/json
Body:
{"commodity":"ONION","district":"BANGALORE","date":"2025-06-15"}

Other endpoints: GET /health, GET /pairs

## Docker
docker build -t price-predictor .
docker run --rm -p 5000:5000 price-predictor

Visit http://127.0.0.1:5000

## CI
Windows CI workflow at .github/workflows/ci.yml installs dependencies and runs basic smoke tests.

## Structure
- src/: Flask app, prediction logic, templates
- models/: Trained model files
- data/: Data folders
- scripts/: Smoke tests

## License
MIT
