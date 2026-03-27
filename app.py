
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Load the trained models and label encoder
with open("models/regressor.pkl", "rb") as f:
    regressor = pickle.load(f)

with open("models/classifier.pkl", "rb") as f:
    classifier = pickle.load(f)

with open("models/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'  # Change this in production
CORS(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create tables if not exist
with app.app_context():
    db.create_all()

# Registration endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials.'}), 401
    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200
@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    try:
        battery_size = float(data["battery_size"])
        brand_name = data["brand_name"]
        memory_size = float(data["memory_size"])
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input."}), 400

    # Encode brand_name
    try:
        brand_name_encoded = label_encoder.transform([brand_name])[0]
    except ValueError:
        return jsonify({"error": "Brand name not recognized!"}), 400

    X_input = np.array([[battery_size, brand_name_encoded, memory_size]])

    try:
        model_name_encoded = classifier.predict(X_input)[0]
        model_name = label_encoder.inverse_transform([model_name_encoded])[0]
    except Exception:
        model_name = "Unknown (unseen in training data)"

    y_pred = regressor.predict(X_input)
    lowest_price = y_pred[0][0]
    highest_price = y_pred[0][1]
    release_date = y_pred[0][2]
    screen_size = y_pred[0][3]
    release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')

    result = {
        "model_name": model_name,
        "lowest_price": round(lowest_price, 2),
        "highest_price": round(highest_price, 2),
        "release_date": release_date,
        "screen_size": round(screen_size, 2)
    }
    return jsonify({"prediction": result})

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
