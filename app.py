from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Storm Backend Running 🚀"

@app.route("/run-model")
def run_model():
    try:
        # run your python script
        result = subprocess.run(
            ["python", "ml/live_predict.py"],
            capture_output=True,
            text=True
        )

        # OPTIONAL: read CSV output
        csv_path = "forecast/output_pred.csv"

        data = {
            "storm_value": "--",
            "solar_wind_speed": "--",
            "density": "--",
            "bz": "--",
            "confidence": "--",
            "logs": result.stdout
        }

        if os.path.exists(csv_path):
            import csv
            with open(csv_path, "r") as f:
                reader = list(csv.reader(f))
                if len(reader) > 1:
                    row = reader[1]
                    headers = reader[0]
                    row_dict = dict(zip(headers, row))
                    data.update(row_dict)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

app.run(host="0.0.0.0", port=10000)
