from datetime import datetime

from flask import Blueprint, request, render_template, current_app

from prediction_routes import _runtime_flags, _predict_with_models
from predict_utils import mock_predict_single


web_bp = Blueprint('web', __name__)


@web_bp.route('/', methods=['GET', 'POST'])
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
