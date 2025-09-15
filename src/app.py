# src/app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from src
sys.path.append(str(Path(__file__).resolve().parent))
from predict import predict_for_date

# Configure template and static folders relative to this file
BASE_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)

# Project root is the parent of src
PROJECT_ROOT = BASE_DIR.parent
MODELS_DIR = PROJECT_ROOT / "models"

def scan_model_pairs():
    """Return a list of available (commodity, district) pairs from models directory.
    Looks for files named like '<commodity>_<district>_arima.pkl'.
    """
    pairs = []
    try:
        for p in MODELS_DIR.glob("*_arima.pkl"):
            name = p.stem  # e.g., 'onion_bangalore_arima'
            if name.endswith("_arima"):
                base = name[: -len("_arima")]  # 'onion_bangalore'
            else:
                parts = name.split("_")
                if len(parts) < 3:
                    continue
                base = "_".join(parts[:-1])
            if "_" in base:
                commodity, district = base.split("_", 1)
                pairs.append((commodity.upper(), district.upper()))
    except FileNotFoundError:
        pass
    # Deduplicate and sort
    pairs = sorted(set(pairs))
    return pairs

def build_pairs_map(pairs=None):
    if pairs is None:
        pairs = scan_model_pairs()
    mapping = {}
    for c, d in pairs:
        mapping.setdefault(c, []).append(d)
    # sort districts for each commodity
    for k in mapping:
        mapping[k] = sorted(set(mapping[k]))
    return mapping

@app.get("/")
def index():
    pairs = scan_model_pairs()
    pairs_map = build_pairs_map(pairs)
    return render_template("index.html", pairs=pairs, pairs_map=pairs_map)

@app.get("/api")
def api_index():
    return jsonify({
        "status": "ok",
        "message": "Price Predictor API",
        "endpoints": ["GET /health", "POST /predict", "GET /"],
    })

@app.get("/pairs")
def get_pairs():
    """Return mapping or filtered list of districts for a commodity.
    - /pairs -> { commodity: [districts] }
    - /pairs?commodity=ONION -> { "ONION": [districts] }
    """
    pairs_map = build_pairs_map()
    commodity = (request.args.get("commodity") or "").strip().upper()
    if commodity:
        if commodity in pairs_map:
            return jsonify({commodity: pairs_map[commodity]})
        return jsonify({commodity: []})
    return jsonify(pairs_map)

@app.get("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}
    commodity = data.get('commodity')
    district = data.get('district')
    date = data.get('date')
    forecast_days = data.get('forecast_days', 7)  # Default to 7 days
    # Basic validation
    missing = [k for k, v in {"commodity": commodity, "district": district, "date": date}.items() if not v]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    try:
        result = predict_for_date(commodity, district, date, forecast_days)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.post("/predict-ui")
def predict_ui():
    # Handle HTML form submission
    commodity = (request.form.get("commodity") or "").strip()
    district = (request.form.get("district") or "").strip()
    date = (request.form.get("date") or "").strip()
    forecast_days = request.form.get("forecast_days") or 7
    try:
        forecast_days = int(forecast_days)
    except Exception:
        forecast_days = 7

    error = None
    missing = [k for k, v in {"commodity": commodity, "district": district, "date": date}.items() if not v]
    if missing:
        error = f"Missing required fields: {', '.join(missing)}"

    result = None
    if not error:
        try:
            result = predict_for_date(commodity, district, date, forecast_days)
        except Exception as e:
            error = str(e)

    return render_template("result.html", error=error, result=result, commodity=commodity, district=district, date=date, forecast_days=forecast_days)

if __name__ == '__main__':
    # Run in a stable, single-process mode bound to localhost
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False, threaded=True)
