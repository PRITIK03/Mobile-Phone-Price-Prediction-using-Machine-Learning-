
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import hashlib
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Load the trained models and label encoder
try:
    with open("models/regressor.pkl", "rb") as f:
        regressor = pickle.load(f)
except FileNotFoundError:
    print("Warning: regressor.pkl not found. Please ensure model files are in the models directory.")
    regressor = None

try:
    with open("models/classifier.pkl", "rb") as f:
        classifier = pickle.load(f)
except FileNotFoundError:
    print("Warning: classifier.pkl not found. Please ensure model files are in the models directory.")
    classifier = None

try:
    with open("models/label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
except FileNotFoundError:
    print("Warning: label_encoder.pkl not found. Please ensure model files are in the models directory.")
    label_encoder = None



app = Flask(__name__)
# Enhanced database configuration with connection pooling
database_url = os.environ.get('DATABASE_URL', 'sqlite:///users.db')

if database_url.startswith('sqlite'):
    # SQLite configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30
    }
else:
    # PostgreSQL/MySQL configuration for production
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 20,           # Number of connections to keep open
        'max_overflow': 30,        # Additional connections when pool is full
        'pool_recycle': 3600,     # Recycle connections every hour
        'pool_pre_ping': True,    # Test connections before use
        'pool_timeout': 30,        # Timeout for getting connection from pool
        'echo': False             # Set to True for SQL logging in development
    }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
import os
import datetime

# Simple in-memory cache (in production, use Redis)
prediction_cache = {}

def get_cache_key(battery_size, brand_name, memory_size):
    """Generate cache key for predictions"""
    data = f"{battery_size}_{brand_name}_{memory_size}"
    return hashlib.md5(data.encode()).hexdigest()

def get_cached_prediction(cache_key):
    """Get cached prediction if available"""
    if cache_key in prediction_cache:
        cached_data = prediction_cache[cache_key]
        # Check if cache is still valid (5 minutes)
        if datetime.now() - cached_data['timestamp'] < timedelta(minutes=5):
            return cached_data['prediction']
    return None

def cache_prediction(cache_key, prediction):
    """Cache prediction result"""
    prediction_cache[cache_key] = {
        'prediction': prediction,
        'timestamp': datetime.now()
    }

def check_database_health():
    """Check database connection health"""
    try:
        # Test database connection
        db.engine.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

@app.before_request
def before_request():
    """Check database health before each request"""
    if not hasattr(app, '_db_health_checked'):
        if not check_database_health():
            print("Warning: Database connection issues detected")
        app._db_health_checked = True

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key_change_in_production')  # Use environment variable in production
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
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Validate input
    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400
    if len(username) < 3 or len(username) > 50:
        return jsonify({'error': 'Username must be 3-50 characters.'}), 400
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters.'}), 400
    if not username.replace('_', '').replace('-', '').isalnum():
        return jsonify({'error': 'Username can only contain letters, numbers, underscores, and hyphens.'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409
    
    try:
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Validate input
    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400
    
    # Rate limiting check (simple implementation)
    # In production, use Redis or database for proper rate limiting
    if hasattr(login, '_attempts'):
        login._attempts = getattr(login, '_attempts', 0) + 1
        if login._attempts > 5:
            return jsonify({'error': 'Too many failed attempts. Please try again later.'}), 429
    else:
        login._attempts = 1
    
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials.'}), 401
    
    # Reset attempts on successful login
    login._attempts = 0
    
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=1))
    return jsonify({'access_token': access_token}), 200
@app.route("/api/predict", methods=["POST"])
def api_predict():
    if not all([regressor, classifier, label_encoder]):
        return jsonify({"error": "Models not loaded. Please check model files."}), 500
    
    data = request.get_json()
    try:
        battery_size = float(data["battery_size"])
        brand_name = data["brand_name"]
        memory_size = float(data["memory_size"])
        
        # Validate input ranges
        if battery_size <= 0 or battery_size > 10000:
            return jsonify({"error": "Battery size must be between 1 and 10000 mAh."}), 400
        if memory_size <= 0 or memory_size > 512:
            return jsonify({"error": "Memory size must be between 1 and 512 GB."}), 400
        if not brand_name or len(brand_name.strip()) == 0:
            return jsonify({"error": "Brand name is required."}), 400
            
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input format."}), 400

    # Check cache first
    cache_key = get_cache_key(battery_size, brand_name.strip(), memory_size)
    cached_result = get_cached_prediction(cache_key)
    if cached_result:
        return jsonify({"prediction": cached_result, "cached": True})

    # Encode brand_name
    try:
        brand_name_encoded = label_encoder.transform([brand_name.strip()])[0]
    except ValueError:
        return jsonify({"error": "Brand name not recognized! Try: Samsung, Apple, Xiaomi, OnePlus, etc."}), 400

    X_input = np.array([[battery_size, brand_name_encoded, memory_size]])

    try:
        model_name_encoded = classifier.predict(X_input)[0]
        model_name = label_encoder.inverse_transform([model_name_encoded])[0]
    except Exception as e:
        print(f"Classifier error: {e}")
        model_name = "Unknown (unseen in training data)"

    try:
        y_pred = regressor.predict(X_input)
        lowest_price = max(0, y_pred[0][0])  # Ensure non-negative
        highest_price = max(0, y_pred[0][1])  # Ensure non-negative
        release_date = y_pred[0][2]
        screen_size = max(1, min(10, y_pred[0][3]))  # Reasonable screen size range
        
        # Convert release date from Unix timestamp to readable date
        try:
            release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')
        except (ValueError, OSError):
            release_date = datetime.now().strftime('%Y-%m-%d')  # Fallback to current date

        result = {
            "model_name": model_name,
            "brand_name": brand_name.strip(),  # Include brand name for frontend
            "lowest_price": round(lowest_price, 2),
            "highest_price": round(highest_price, 2),
            "release_date": release_date,
            "screen_size": round(screen_size, 2)
        }
        
        # Cache the result
        cache_prediction(cache_key, result)
        
        return jsonify({"prediction": result, "cached": False})
    except Exception as e:
        print(f"Regressor error: {e}")
        return jsonify({"error": "Prediction failed. Please try again."}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with database status"""
    db_status = check_database_health()
    cache_size = len(prediction_cache)
    
    return jsonify({
        'status': 'healthy' if db_status else 'unhealthy',
        'database': 'connected' if db_status else 'disconnected',
        'cache_size': cache_size,
        'models_loaded': all([regressor, classifier, label_encoder]),
        'timestamp': datetime.now().isoformat()
    })

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not all([regressor, classifier, label_encoder]):
            return render_template("index.html", result={"error": "Models not loaded. Please check model files."})
        
        try:
            # Get input values from the form
            battery_size = float(request.form["battery_size"])
            brand_name = request.form["brand_name"]
            memory_size = float(request.form["memory_size"])
            
            # Validate input ranges
            if battery_size <= 0 or battery_size > 10000:
                return render_template("index.html", result={"error": "Battery size must be between 1 and 10000 mAh."})
            if memory_size <= 0 or memory_size > 512:
                return render_template("index.html", result={"error": "Memory size must be between 1 and 512 GB."})
            if not brand_name or len(brand_name.strip()) == 0:
                return render_template("index.html", result={"error": "Brand name is required."})

            # Encode brand_name
            try:
                brand_name_encoded = label_encoder.transform([brand_name.strip()])[0]
            except ValueError:
                return render_template("index.html", result={"error": "Brand name not recognized! Try: Samsung, Apple, Xiaomi, OnePlus, etc."})

            # Create feature array for prediction
            X_input = np.array([[battery_size, brand_name_encoded, memory_size]])

            # Predict the model name
            try:
                model_name_encoded = classifier.predict(X_input)[0]
                model_name = label_encoder.inverse_transform([model_name_encoded])[0]
            except Exception as e:
                print(f"Classifier error: {e}")
                model_name = "Unknown (unseen in training data)"

            # Predict other details (price, release date, screen size)
            try:
                y_pred = regressor.predict(X_input)
                lowest_price = max(0, y_pred[0][0])  # Ensure non-negative
                highest_price = max(0, y_pred[0][1])  # Ensure non-negative
                release_date = y_pred[0][2]
                screen_size = max(1, min(10, y_pred[0][3]))  # Reasonable screen size range

                # Convert release date from Unix timestamp to a readable date format
                try:
                    release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')
                except (ValueError, OSError):
                    release_date = datetime.now().strftime('%Y-%m-%d')  # Fallback to current date

                # Prepare results
                result = {
                    "model_name": model_name,
                    "brand_name": brand_name.strip(),  # Include brand name for frontend
                    "lowest_price": round(lowest_price, 2),
                    "highest_price": round(highest_price, 2),
                    "release_date": release_date,
                    "screen_size": round(screen_size, 2)
                }

                # Return results to the template
                return render_template("index.html", result=result)
            except Exception as e:
                print(f"Regressor error: {e}")
                return render_template("index.html", result={"error": "Prediction failed. Please try again."})
                
        except (ValueError, TypeError, KeyError):
            return render_template("index.html", result={"error": "Invalid input format."})

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
