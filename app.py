
from flask import Flask, render_template, request, jsonify, send_file, make_response
from flask_cors import CORS
import numpy as np
import pickle
import hashlib
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import io
import pandas as pd
import csv

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

# Prediction History model
class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Allow anonymous predictions
    battery_size = db.Column(db.Float, nullable=False)
    brand_name = db.Column(db.String(50), nullable=False)
    memory_size = db.Column(db.Float, nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)
    highest_price = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String(20), nullable=False)
    screen_size = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = db.relationship('User', backref=db.backref('predictions', lazy=True))

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
        
        # Save prediction to database (optional - allow anonymous predictions)
        try:
            # Get user from JWT token if available
            auth_header = request.headers.get('Authorization')
            user_id = None
            if auth_header and auth_header.startswith('Bearer '):
                try:
                    from flask_jwt_extended import decode_token
                    token = auth_header.split(' ')[1]
                    decoded_token = decode_token(token)
                    username = decoded_token['sub']
                    user = User.query.filter_by(username=username).first()
                    user_id = user.id if user else None
                except:
                    pass  # Continue without user if token is invalid
            
            # Save prediction history
            prediction = PredictionHistory(
                user_id=user_id,
                battery_size=battery_size,
                brand_name=brand_name.strip(),
                memory_size=memory_size,
                model_name=model_name,
                lowest_price=lowest_price,
                highest_price=highest_price,
                release_date=release_date,
                screen_size=screen_size
            )
            db.session.add(prediction)
            db.session.commit()
        except Exception as e:
            print(f"Failed to save prediction history: {e}")
            db.session.rollback()
        
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

@app.route('/api/predictions/history', methods=['GET'])
@jwt_required()
def get_prediction_history():
    """Get user's prediction history"""
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        limit = min(per_page, 50)  # Max 50 records per page
        
        # Get user's predictions
        predictions = PredictionHistory.query.filter_by(user_id=user.id)\
            .order_by(PredictionHistory.created_at.desc())\
            .paginate(page=page, per_page=limit, error_out=False)
        
        history_data = []
        for prediction in predictions.items:
            history_data.append({
                'id': prediction.id,
                'battery_size': prediction.battery_size,
                'brand_name': prediction.brand_name,
                'memory_size': prediction.memory_size,
                'model_name': prediction.model_name,
                'lowest_price': prediction.lowest_price,
                'highest_price': prediction.highest_price,
                'release_date': prediction.release_date,
                'screen_size': prediction.screen_size,
                'created_at': prediction.created_at.isoformat()
            })
        
        return jsonify({
            'predictions': history_data,
            'pagination': {
                'page': page,
                'per_page': limit,
                'total': predictions.total,
                'pages': predictions.pages,
                'has_next': predictions.has_next,
                'has_prev': predictions.has_prev
            }
        })
        
    except Exception as e:
        print(f"Error fetching prediction history: {e}")
        return jsonify({'error': 'Failed to fetch prediction history'}), 500

@app.route('/api/predictions/<int:prediction_id>', methods=['DELETE'])
@jwt_required()
def delete_prediction(prediction_id):
    """Delete a specific prediction from history"""
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        prediction = PredictionHistory.query.filter_by(id=prediction_id, user_id=user.id).first()
        if not prediction:
            return jsonify({'error': 'Prediction not found'}), 404
        
        db.session.delete(prediction)
        db.session.commit()
        
        return jsonify({'message': 'Prediction deleted successfully'})
        
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete prediction'}), 500

@app.route('/api/predictions/stats', methods=['GET'])
@jwt_required()
def get_prediction_stats():
    """Get user's prediction statistics"""
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get statistics
        total_predictions = PredictionHistory.query.filter_by(user_id=user.id).count()
        
        # Brand preferences
        brand_stats = db.session.query(
            PredictionHistory.brand_name,
            db.func.count(PredictionHistory.id).label('count')
        ).filter_by(user_id=user.id)\
         .group_by(PredictionHistory.brand_name)\
         .order_by(db.desc('count'))\
         .limit(5).all()
        
        # Average price ranges
        avg_low = db.session.query(db.func.avg(PredictionHistory.lowest_price))\
                          .filter_by(user_id=user.id).scalar() or 0
        avg_high = db.session.query(db.func.avg(PredictionHistory.highest_price))\
                           .filter_by(user_id=user.id).scalar() or 0
        
        return jsonify({
            'total_predictions': total_predictions,
            'brand_preferences': [{'brand': brand, 'count': count} for brand, count in brand_stats],
            'average_price_range': {
                'lowest': round(avg_low, 2),
                'highest': round(avg_high, 2)
            }
        })
        
    except Exception as e:
        print(f"Error fetching prediction stats: {e}")
        return jsonify({'error': 'Failed to fetch prediction statistics'}), 500

@app.route('/api/compare', methods=['POST'])
def compare_phones():
    """Compare multiple phones side by side"""
    if not all([regressor, classifier, label_encoder]):
        return jsonify({"error": "Models not loaded. Please check model files."}), 500
    
    data = request.get_json()
    phones = data.get('phones', [])
    
    # Validate input
    if not phones or len(phones) < 2:
        return jsonify({"error": "Please provide at least 2 phones to compare."}), 400
    if len(phones) > 5:
        return jsonify({"error": "Maximum 5 phones can be compared at once."}), 400
    
    comparisons = []
    
    for phone in phones:
        try:
            battery_size = float(phone.get("battery_size"))
            brand_name = phone.get("brand_name")
            memory_size = float(phone.get("memory_size"))
            
            # Validate input ranges
            if battery_size <= 0 or battery_size > 10000:
                return jsonify({"error": f"Battery size must be between 1 and 10000 mAh for phone {phone.get('name', 'unknown')}."}), 400
            if memory_size <= 0 or memory_size > 512:
                return jsonify({"error": f"Memory size must be between 1 and 512 GB for phone {phone.get('name', 'unknown')}."}), 400
            if not brand_name or len(brand_name.strip()) == 0:
                return jsonify({"error": f"Brand name is required for phone {phone.get('name', 'unknown')}."}), 400
            
            # Check cache
            cache_key = get_cache_key(battery_size, brand_name.strip(), memory_size)
            cached_result = get_cached_prediction(cache_key)
            
            if cached_result:
                comparison = {
                    'name': phone.get('name', f'Phone {len(comparisons) + 1}'),
                    'prediction': cached_result,
                    'cached': True
                }
            else:
                # Encode brand_name
                try:
                    brand_name_encoded = label_encoder.transform([brand_name.strip()])[0]
                except ValueError:
                    return jsonify({"error": f"Brand name '{brand_name}' not recognized for phone {phone.get('name', 'unknown')}."}), 400
                
                X_input = np.array([[battery_size, brand_name_encoded, memory_size]])
                
                try:
                    model_name_encoded = classifier.predict(X_input)[0]
                    model_name = label_encoder.inverse_transform([model_name_encoded])[0]
                except Exception as e:
                    print(f"Classifier error: {e}")
                    model_name = "Unknown (unseen in training data)"
                
                try:
                    y_pred = regressor.predict(X_input)
                    lowest_price = max(0, y_pred[0][0])
                    highest_price = max(0, y_pred[0][1])
                    release_date = y_pred[0][2]
                    screen_size = max(1, min(10, y_pred[0][3]))
                    
                    try:
                        release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')
                    except (ValueError, OSError):
                        release_date = datetime.now().strftime('%Y-%m-%d')
                    
                    result = {
                        "model_name": model_name,
                        "brand_name": brand_name.strip(),
                        "lowest_price": round(lowest_price, 2),
                        "highest_price": round(highest_price, 2),
                        "release_date": release_date,
                        "screen_size": round(screen_size, 2)
                    }
                    
                    # Cache the result
                    cache_prediction(cache_key, result)
                    
                    comparison = {
                        'name': phone.get('name', f'Phone {len(comparisons) + 1}'),
                        'prediction': result,
                        'cached': False
                    }
                except Exception as e:
                    print(f"Regressor error: {e}")
                    return jsonify({"error": f"Prediction failed for phone {phone.get('name', 'unknown')}."}), 500
            
            comparisons.append(comparison)
            
        except (KeyError, ValueError, TypeError) as e:
            return jsonify({"error": f"Invalid input format for phone {phone.get('name', 'unknown')}: {str(e)}"}), 400
    
    # Calculate comparison metrics
    comparison_metrics = {
        'cheapest': min(comparisons, key=lambda x: x['prediction']['lowest_price']),
        'most_expensive': max(comparisons, key=lambda x: x['prediction']['highest_price']),
        'best_battery': max(comparisons, key=lambda x: x['prediction']['brand_name']),
        'largest_screen': max(comparisons, key=lambda x: x['prediction']['screen_size'])
    }
    
    return jsonify({
        'comparisons': comparisons,
        'metrics': {
            'cheapest': comparison_metrics['cheapest']['name'],
            'most_expensive': comparison_metrics['most_expensive']['name'],
            'largest_screen': comparison_metrics['largest_screen']['name']
        },
        'count': len(comparisons)
    })


@app.route('/api/predict/batch', methods=['POST'])
def api_predict_batch():
    """Accept a CSV file upload with columns: battery_size, brand_name, memory_size
    Returns a CSV file with predictions appended: model_name, lowest_price, highest_price, release_date, screen_size
    """
    if not all([regressor, classifier, label_encoder]):
        return jsonify({"error": "Models not loaded. Please check model files."}), 500

    # Accept multipart file upload
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({"error": "No file uploaded. Please upload a CSV file under field 'file'."}), 400

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {e}"}), 400

    # Normalize column names
    cols = {c.lower(): c for c in df.columns}
    required = ['battery_size', 'brand_name', 'memory_size']
    for r in required:
        if r not in cols:
            return jsonify({"error": f"Missing required column: {r}"}), 400

    # Prepare output rows
    output_rows = []

    for idx, row in df.iterrows():
        try:
            battery_size = float(row[cols['battery_size']])
            brand_name = str(row[cols['brand_name']])
            memory_size = float(row[cols['memory_size']])

            # basic validation
            if battery_size <= 0 or battery_size > 10000:
                raise ValueError('battery_size out of range')
            if memory_size <= 0 or memory_size > 512:
                raise ValueError('memory_size out of range')

            # Encode brand
            try:
                brand_name_encoded = label_encoder.transform([brand_name.strip()])[0]
            except Exception:
                model_name = 'Unknown (brand not recognized)'
                result = {
                    'model_name': model_name,
                    'brand_name': brand_name.strip(),
                    'lowest_price': None,
                    'highest_price': None,
                    'release_date': None,
                    'screen_size': None,
                    'error': 'brand not recognized'
                }
                output_rows.append({**row.to_dict(), **result})
                continue

            X_input = np.array([[battery_size, brand_name_encoded, memory_size]])

            try:
                model_name_encoded = classifier.predict(X_input)[0]
                model_name = label_encoder.inverse_transform([model_name_encoded])[0]
            except Exception:
                model_name = 'Unknown (classifier error)'

            y_pred = regressor.predict(X_input)
            lowest_price = max(0, y_pred[0][0])
            highest_price = max(0, y_pred[0][1])
            release_date = y_pred[0][2]
            screen_size = max(1, min(10, y_pred[0][3]))
            try:
                release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')
            except Exception:
                release_date = None

            result = {
                'model_name': model_name,
                'brand_name': brand_name.strip(),
                'lowest_price': round(lowest_price, 2),
                'highest_price': round(highest_price, 2),
                'release_date': release_date,
                'screen_size': round(screen_size, 2),
                'error': None
            }

            # Save history (anonymous)
            try:
                prediction = PredictionHistory(
                    user_id=None,
                    battery_size=battery_size,
                    brand_name=brand_name.strip(),
                    memory_size=memory_size,
                    model_name=model_name,
                    lowest_price=lowest_price,
                    highest_price=highest_price,
                    release_date=release_date or '',
                    screen_size=screen_size
                )
                db.session.add(prediction)
                # commit at the end (bulk)
            except Exception as e:
                print(f"Failed to queue prediction history: {e}")

            output_rows.append({**row.to_dict(), **result})

        except Exception as e:
            output_rows.append({**row.to_dict(), 'model_name': None, 'lowest_price': None, 'highest_price': None, 'release_date': None, 'screen_size': None, 'error': str(e)})

    # Try to commit any queued history entries
    try:
        db.session.commit()
    except Exception as e:
        print(f"Failed to commit batch prediction history: {e}")
        db.session.rollback()

    out_df = pd.DataFrame(output_rows)

    # Prepare CSV for download
    csv_buffer = io.StringIO()
    out_df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    buf = io.BytesIO(csv_bytes)
    buf.seek(0)

    filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(buf, mimetype='text/csv', as_attachment=True, download_name=filename)

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
