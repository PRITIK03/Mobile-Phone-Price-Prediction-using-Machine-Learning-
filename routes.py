from flask import Blueprint, request, jsonify, current_app, send_file, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db, bcrypt, jwt
from models import User, PredictionHistory
from predict_utils import get_cache_key, get_cached_prediction, cache_prediction, mock_predict_single, prediction_cache
import numpy as np
import pandas as pd
import io
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400
    if len(username) < 3 or len(username) > 50:
        return jsonify({'error': 'Username must be 3-50 characters.'}), 400
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters.'}), 400
    if not username.replace('_', '').replace('-', '').isalnum():
        return jsonify({'error': 'Username can only contain letters, numbers, underscores, and hyphens.'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409
    try:
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully.'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400
    if hasattr(login, '_attempts'):
        login._attempts = getattr(login, '_attempts', 0) + 1
        if login._attempts > 5:
            return jsonify({'error': 'Too many failed attempts. Please try again later.'}), 429
    else:
        login._attempts = 1
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials.'}), 401
    login._attempts = 0
    access_token = create_access_token(identity=username, expires_delta=current_app.config.get('TOKEN_EXPIRES_DELTA'))
    return jsonify({'access_token': access_token}), 200

@api_bp.route('/predict', methods=['POST'])
def api_predict():
    models_loaded = getattr(current_app, 'models_loaded', False)
    MOCK_MODE = getattr(current_app, 'MOCK_MODE', False)
    regressor = getattr(current_app, 'regressor', None)
    classifier = getattr(current_app, 'classifier', None)
    label_encoder = getattr(current_app, 'label_encoder', None)

    if not models_loaded and not MOCK_MODE:
        return jsonify({"error": "Models not loaded. Please check model files or enable MOCK_MODE."}), 500
    data = request.get_json()
    try:
        battery_size = float(data["battery_size"])
        brand_name = data["brand_name"]
        memory_size = float(data["memory_size"])
        if battery_size <= 0 or battery_size > 10000:
            return jsonify({"error": "Battery size must be between 1 and 10000 mAh."}), 400
        if memory_size <= 0 or memory_size > 512:
            return jsonify({"error": "Memory size must be between 1 and 512 GB."}), 400
        if not brand_name or len(brand_name.strip()) == 0:
            return jsonify({"error": "Brand name is required."}), 400
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input format."}), 400
    cache_key = get_cache_key(battery_size, brand_name.strip(), memory_size)
    cached_result = get_cached_prediction(cache_key)
    if cached_result:
        return jsonify({"prediction": cached_result, "cached": True})
    if not models_loaded and MOCK_MODE:
        result = mock_predict_single(battery_size, brand_name, memory_size)
        cache_prediction(cache_key, result)
        return jsonify({"prediction": result, "cached": False})
    try:
        brand_name_encoded = label_encoder.transform([brand_name.strip()])[0]
    except ValueError:
        return jsonify({"error": "Brand name not recognized! Try: Samsung, Apple, Xiaomi, OnePlus, etc."}), 400
    X_input = np.array([[battery_size, brand_name_encoded, memory_size]])
    try:
        model_name_encoded = classifier.predict(X_input)[0]
        model_name = label_encoder.inverse_transform([model_name_encoded])[0]
    except Exception:
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
        cache_prediction(cache_key, result)
        try:
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
                    pass
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

@api_bp.route('/health', methods=['GET'])
def health_check():
    db_status = True
    try:
        db.engine.execute("SELECT 1")
    except Exception:
        db_status = False
    cache_size = len(prediction_cache)
    models_loaded = getattr(current_app, 'models_loaded', False)
    return jsonify({
        'status': 'healthy' if db_status else 'unhealthy',
        'database': 'connected' if db_status else 'disconnected',
        'cache_size': cache_size,
        'models_loaded': models_loaded,
        'timestamp': datetime.now().isoformat()
    })

@api_bp.route('/predictions/history', methods=['GET'])
@jwt_required()
def get_prediction_history():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        limit = min(per_page, 50)
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

@api_bp.route('/predictions/<int:prediction_id>', methods=['DELETE'])
@jwt_required()
def delete_prediction(prediction_id):
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

@api_bp.route('/predictions/stats', methods=['GET'])
@jwt_required()
def get_prediction_stats():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        total_predictions = PredictionHistory.query.filter_by(user_id=user.id).count()
        brand_stats = db.session.query(
            PredictionHistory.brand_name,
            db.func.count(PredictionHistory.id).label('count')
        ).filter_by(user_id=user.id)\
         .group_by(PredictionHistory.brand_name)\
         .order_by(db.desc('count'))\
         .limit(5).all()
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

@api_bp.route('/compare', methods=['POST'])
def compare_phones():
    models_loaded = getattr(current_app, 'models_loaded', False)
    MOCK_MODE = getattr(current_app, 'MOCK_MODE', False)
    regressor = getattr(current_app, 'regressor', None)
    classifier = getattr(current_app, 'classifier', None)
    label_encoder = getattr(current_app, 'label_encoder', None)
    if not models_loaded and not MOCK_MODE:
        return jsonify({"error": "Models not loaded. Please check model files or enable MOCK_MODE."}), 500
    data = request.get_json()
    phones = data.get('phones', [])
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
            if battery_size <= 0 or battery_size > 10000:
                return jsonify({"error": f"Battery size must be between 1 and 10000 mAh for phone {phone.get('name', 'unknown')}."}), 400
            if memory_size <= 0 or memory_size > 512:
                return jsonify({"error": f"Memory size must be between 1 and 512 GB for phone {phone.get('name', 'unknown')}."}), 400
            if not brand_name or len(brand_name.strip()) == 0:
                return jsonify({"error": f"Brand name is required for phone {phone.get('name', 'unknown')}."}), 400
            cache_key = get_cache_key(battery_size, brand_name.strip(), memory_size)
            cached_result = get_cached_prediction(cache_key)
            if cached_result:
                comparison = {
                    'name': phone.get('name', f'Phone {len(comparisons) + 1}'),
                    'battery_size': battery_size,
                    'memory_size': memory_size,
                    'prediction': cached_result,
                    'cached': True
                }
            else:
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
                    cache_prediction(cache_key, result)
                    comparison = {
                        'name': phone.get('name', f'Phone {len(comparisons) + 1}'),
                        'battery_size': battery_size,
                        'memory_size': memory_size,
                        'prediction': result,
                        'cached': False
                    }
                except Exception as e:
                    print(f"Regressor error: {e}")
                    return jsonify({"error": f"Prediction failed for phone {phone.get('name', 'unknown')}."}), 500
            comparisons.append(comparison)
        except (KeyError, ValueError, TypeError) as e:
            return jsonify({"error": f"Invalid input format for phone {phone.get('name', 'unknown')}: {str(e)}"}), 400
    comparison_metrics = {
        'cheapest': min(comparisons, key=lambda x: x['prediction']['lowest_price']),
        'most_expensive': max(comparisons, key=lambda x: x['prediction']['highest_price']),
        'best_battery': max(comparisons, key=lambda x: x.get('battery_size', 0)),
        'largest_screen': max(comparisons, key=lambda x: x['prediction']['screen_size'])
    }
    return jsonify({
        'comparisons': comparisons,
        'metrics': {
            'cheapest': comparison_metrics['cheapest']['name'],
            'most_expensive': comparison_metrics['most_expensive']['name'],
            'best_battery': comparison_metrics['best_battery']['name'],
            'largest_screen': comparison_metrics['largest_screen']['name']
        },
        'count': len(comparisons)
    })

@api_bp.route('/predict/batch', methods=['POST'])
def api_predict_batch():
    models_loaded = getattr(current_app, 'models_loaded', False)
    MOCK_MODE = getattr(current_app, 'MOCK_MODE', False)
    if not models_loaded and not MOCK_MODE:
        return jsonify({"error": "Models not loaded. Please check model files or enable MOCK_MODE."}), 500
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({"error": "No file uploaded. Please upload a CSV file under field 'file'."}), 400
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {e}"}), 400
    cols = {c.lower(): c for c in df.columns}
    required = ['battery_size', 'brand_name', 'memory_size']
    for r in required:
        if r not in cols:
            return jsonify({"error": f"Missing required column: {r}"}), 400
    output_rows = []
    for idx, row in df.iterrows():
        try:
            battery_size = float(row[cols['battery_size']])
            brand_name = str(row[cols['brand_name']])
            memory_size = float(row[cols['memory_size']])
            if battery_size <= 0 or battery_size > 10000:
                raise ValueError('battery_size out of range')
            if memory_size <= 0 or memory_size > 512:
                raise ValueError('memory_size out of range')
            try:
                brand_name_encoded = current_app.label_encoder.transform([brand_name.strip()])[0]
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
                model_name_encoded = current_app.classifier.predict(X_input)[0]
                model_name = current_app.label_encoder.inverse_transform([model_name_encoded])[0]
            except Exception:
                model_name = 'Unknown (classifier error)'
            y_pred = current_app.regressor.predict(X_input)
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
            except Exception as e:
                print(f"Failed to queue prediction history: {e}")
            output_rows.append({**row.to_dict(), **result})
        except Exception as e:
            output_rows.append({**row.to_dict(), 'model_name': None, 'lowest_price': None, 'highest_price': None, 'release_date': None, 'screen_size': None, 'error': str(e)})
    try:
        db.session.commit()
    except Exception as e:
        print(f"Failed to commit batch prediction history: {e}")
        db.session.rollback()
    out_df = pd.DataFrame(output_rows)
    csv_buffer = io.StringIO()
    out_df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    buf = io.BytesIO(csv_bytes)
    buf.seek(0)
    filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(buf, mimetype='text/csv', as_attachment=True, download_name=filename)

@api_bp.route('/', methods=['GET', 'POST'])
def index():
    current_year = datetime.now().year
    if request.method == 'POST':
        if not getattr(current_app, 'models_loaded', False) and not getattr(current_app, 'MOCK_MODE', False):
            return render_template('index.html', result={"error": "Models not loaded. Please check model files."}, current_year=current_year)
        try:
            battery_size = float(request.form['battery_size'])
            brand_name = request.form['brand_name']
            memory_size = float(request.form['memory_size'])
            if battery_size <= 0 or battery_size > 10000:
                return render_template('index.html', result={"error": "Battery size must be between 1 and 10000 mAh."}, current_year=current_year)
            if memory_size <= 0 or memory_size > 512:
                return render_template('index.html', result={"error": "Memory size must be between 1 and 512 GB."}, current_year=current_year)
            if not brand_name or len(brand_name.strip()) == 0:
                return render_template('index.html', result={"error": "Brand name is required."}, current_year=current_year)
            try:
                brand_name_encoded = current_app.label_encoder.transform([brand_name.strip()])[0]
            except Exception:
                return render_template('index.html', result={"error": "Brand name not recognized! Try: Samsung, Apple, Xiaomi, OnePlus, etc."}, current_year=current_year)
            X_input = np.array([[battery_size, brand_name_encoded, memory_size]])
            try:
                model_name_encoded = current_app.classifier.predict(X_input)[0]
                model_name = current_app.label_encoder.inverse_transform([model_name_encoded])[0]
            except Exception as e:
                print(f"Classifier error: {e}")
                model_name = "Unknown (unseen in training data)"
            try:
                y_pred = current_app.regressor.predict(X_input)
                lowest_price = max(0, y_pred[0][0])
                highest_price = max(0, y_pred[0][1])
                release_date = y_pred[0][2]
                screen_size = max(1, min(10, y_pred[0][3]))
                try:
                    release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')
                except (ValueError, OSError):
                    release_date = datetime.now().strftime('%Y-%m-%d')
                result = {
                    'model_name': model_name,
                    'brand_name': brand_name.strip(),
                    'lowest_price': round(lowest_price, 2),
                    'highest_price': round(highest_price, 2),
                    'release_date': release_date,
                    'screen_size': round(screen_size, 2)
                }
                return render_template('index.html', result=result, current_year=current_year)
            except Exception as e:
                print(f"Regressor error: {e}")
                return render_template('index.html', result={"error": "Prediction failed. Please try again."}, current_year=current_year)
        except (ValueError, TypeError, KeyError):
            return render_template('index.html', result={"error": "Invalid input format."}, current_year=current_year)
    return render_template('index.html', current_year=current_year)
