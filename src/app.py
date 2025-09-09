# src/app.py
from flask import Flask, request, jsonify
from predict import predict_for_date

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    commodity = data.get('commodity')
    district = data.get('district')
    date = data.get('date')
    try:
        result = predict_for_date(commodity, district, date)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
