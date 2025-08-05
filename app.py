from flask import Flask, render_template, request
import numpy as np
import pickle
from datetime import datetime

# Load the trained models and label encoder
with open("models/regressor.pkl", "rb") as f:
    regressor = pickle.load(f)

with open("models/classifier.pkl", "rb") as f:
    classifier = pickle.load(f)

with open("models/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get input values from the form
        battery_size = float(request.form["battery_size"])
        brand_name = request.form["brand_name"]
        memory_size = float(request.form["memory_size"])

        # Encode brand_name
        try:
            brand_name_encoded = label_encoder.transform([brand_name])[0]
        except ValueError:
            return render_template("index.html", result={"error": "Brand name not recognized!"})

        # Create feature array for prediction
        X_input = np.array([[battery_size, brand_name_encoded, memory_size]])

        # Predict the model name
        try:
            model_name_encoded = classifier.predict(X_input)[0]
            model_name = label_encoder.inverse_transform([model_name_encoded])[0]
        except ValueError:
            # Handle unseen label
            model_name = "Unknown (unseen in training data)"

        # Predict other details (price, release date, screen size)
        y_pred = regressor.predict(X_input)

        # Get predicted values
        lowest_price = y_pred[0][0]
        highest_price = y_pred[0][1]
        release_date = y_pred[0][2]
        screen_size = y_pred[0][3]

        # Convert release date from Unix timestamp to a readable date format
        release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')

        # Prepare results
        result = {
            "model_name": model_name,
            "lowest_price": round(lowest_price, 2),
            "highest_price": round(highest_price, 2),
            "release_date": release_date,
            "screen_size": round(screen_size, 2)
        }

        # Return results to the template
        return render_template("index.html", result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
