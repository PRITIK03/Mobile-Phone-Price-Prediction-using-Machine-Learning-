from datetime import datetime
import io

import numpy as np
import pandas as pd
from flask import Blueprint, request, jsonify, current_app, send_file, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token

from extensions import db
from models import PredictionHistory, User
from predict_utils import get_cache_key, get_cached_prediction, cache_prediction, mock_predict_single


predictions_bp = Blueprint('predictions', __name__)


def _runtime_flags():
    return {
        'models_loaded': getattr(current_app, 'models_loaded', False),
        'mock_mode': getattr(current_app, 'MOCK_MODE', False),
        'regressor': getattr(current_app, 'regressor', None),
        'classifier': getattr(current_app, 'classifier', None),
        'label_encoder': getattr(current_app, 'label_encoder', None),
    }


def _predict_with_models(battery_size, brand_name, memory_size):
    flags = _runtime_flags()
    regressor = flags['regressor']
    classifier = flags['classifier']
    label_encoder = flags['label_encoder']

    brand_name_encoded = label_encoder.transform([brand_name.strip()])[0]
    X_input = np.array([[battery_size, brand_name_encoded, memory_size]])

    model_name_encoded = classifier.predict(X_input)[0]
    model_name = label_encoder.inverse_transform([model_name_encoded])[0]

    y_pred = regressor.predict(X_input)
    lowest_price = max(0, y_pred[0][0])
    highest_price = max(0, y_pred[0][1])
    release_date = y_pred[0][2]
    screen_size = max(1, min(10, y_pred[0][3]))
    try:
        release_date = datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d')
    except (ValueError, OSError):
        release_date = datetime.now().strftime('%Y-%m-%d')

    return {
        'model_name': model_name,
        'brand_name': brand_name.strip(),
        'lowest_price': round(lowest_price, 2),
        'highest_price': round(highest_price, 2),
        'release_date': release_date,
        'screen_size': round(screen_size, 2),
    }


@predictions_bp.route('/', methods=['GET', 'POST'])
def index():
    current_year = datetime.now().year
    if request.method == 'POST':
        flags = _runtime_flags()
        if not flags['models_loaded'] and not flags['mock_mode']:
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

            if not flags['models_loaded'] and flags['mock_mode']:
                result = mock_predict_single(battery_size, brand_name, memory_size)
                return render_template('index.html', result=result, current_year=current_year)

            result = _predict_with_models(battery_size, brand_name, memory_size)
            return render_template('index.html', result=result, current_year=current_year)
        except ValueError:
            return render_template('index.html', result={"error": "Invalid input format."}, current_year=current_year)
        except Exception as e:
            print(f"Prediction error: {e}")
            return render_template('index.html', result={"error": "Prediction failed. Please try again."}, current_year=current_year)

    return render_template('index.html', current_year=current_year)


@predictions_bp.route('/predict', methods=['POST'])
def api_predict():
    flags = _runtime_flags()
    if not flags['models_loaded'] and not flags['mock_mode']:
        return jsonify({"error": "Models not loaded. Please check model files or enable MOCK_MODE."}), 500

    data = request.get_json() or {}
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

    if not flags['models_loaded'] and flags['mock_mode']:
        result = mock_predict_single(battery_size, brand_name, memory_size)
        cache_prediction(cache_key, result)
        return jsonify({"prediction": result, "cached": False})

    try:
        result = _predict_with_models(battery_size, brand_name, memory_size)
        cache_prediction(cache_key, result)

        try:
            auth_header = request.headers.get('Authorization')
            user_id = None
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                decoded_token = decode_token(token)
                username = decoded_token['sub']
                user = User.query.filter_by(username=username).first()
                user_id = user.id if user else None

            prediction = PredictionHistory(
                user_id=user_id,
                battery_size=battery_size,
                brand_name=brand_name.strip(),
                memory_size=memory_size,
                model_name=result['model_name'],
                lowest_price=result['lowest_price'],
                highest_price=result['highest_price'],
                release_date=result['release_date'],
                screen_size=result['screen_size']
            )
            db.session.add(prediction)
            db.session.commit()
        except Exception as e:
            print(f"Failed to save prediction history: {e}")
            db.session.rollback()

        return jsonify({"prediction": result, "cached": False})
    except ValueError:
        return jsonify({"error": "Brand name not recognized! Try: Samsung, Apple, Xiaomi, OnePlus, etc."}), 400
    except Exception as e:
        print(f"Regressor error: {e}")
        return jsonify({"error": "Prediction failed. Please try again."}), 500


@predictions_bp.route('/compare', methods=['POST'])
def compare_phones():
    flags = _runtime_flags()
    if not flags['models_loaded'] and not flags['mock_mode']:
        return jsonify({"error": "Models not loaded. Please check model files or enable MOCK_MODE."}), 500

    data = request.get_json() or {}
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
                if not flags['models_loaded'] and flags['mock_mode']:
                    result = mock_predict_single(battery_size, brand_name, memory_size)
                else:
                    result = _predict_with_models(battery_size, brand_name, memory_size)
                cache_prediction(cache_key, result)
                comparison = {
                    'name': phone.get('name', f'Phone {len(comparisons) + 1}'),
                    'battery_size': battery_size,
                    'memory_size': memory_size,
                    'prediction': result,
                    'cached': False
                }

            comparisons.append(comparison)
        except (KeyError, ValueError, TypeError) as e:
            return jsonify({"error": f"Invalid input format for phone {phone.get('name', 'unknown')}: {str(e)}"}), 400
        except Exception as e:
            print(f"Comparison error: {e}")
            return jsonify({"error": f"Prediction failed for phone {phone.get('name', 'unknown')}."}), 500

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


@predictions_bp.route('/predict/batch', methods=['POST'])
def api_predict_batch():
    flags = _runtime_flags()
    if not flags['models_loaded'] and not flags['mock_mode']:
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
    for _, row in df.iterrows():
        try:
            battery_size = float(row[cols['battery_size']])
            brand_name = str(row[cols['brand_name']])
            memory_size = float(row[cols['memory_size']])

            if battery_size <= 0 or battery_size > 10000:
                raise ValueError('battery_size out of range')
            if memory_size <= 0 or memory_size > 512:
                raise ValueError('memory_size out of range')

            if not flags['models_loaded'] and flags['mock_mode']:
                result = mock_predict_single(battery_size, brand_name, memory_size)
            else:
                result = _predict_with_models(battery_size, brand_name, memory_size)

            result['error'] = None
            try:
                prediction = PredictionHistory(
                    user_id=None,
                    battery_size=battery_size,
                    brand_name=brand_name.strip(),
                    memory_size=memory_size,
                    model_name=result['model_name'],
                    lowest_price=result['lowest_price'],
                    highest_price=result['highest_price'],
                    release_date=result['release_date'],
                    screen_size=result['screen_size']
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
    buf = io.BytesIO(csv_buffer.getvalue().encode('utf-8'))
    buf.seek(0)
    filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(buf, mimetype='text/csv', as_attachment=True, download_name=filename)
