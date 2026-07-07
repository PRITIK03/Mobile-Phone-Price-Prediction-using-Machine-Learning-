import hashlib
from datetime import datetime, timedelta
import io

# Simple in-memory cache (in production, replace with Redis)
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


def mock_predict_single(battery_size, brand_name, memory_size):
    """Return a deterministic mock prediction when real models aren't available."""
    base = 200 + (battery_size * 0.5) + (memory_size * 20)
    lowest_price = max(100, base)
    highest_price = lowest_price * 1.25
    # release_date as current timestamp
    release_date = int(datetime.now().timestamp())
    # screen size heuristic
    screen_size = round(4.7 + min(3.0, (memory_size / 256.0) * 2.5), 2)
    model_name = f"{brand_name.strip()} Model {int(memory_size)}GB"
    return {
        'model_name': model_name,
        'brand_name': brand_name.strip(),
        'lowest_price': round(lowest_price, 2),
        'highest_price': round(highest_price, 2),
        'release_date': datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%d'),
        'screen_size': screen_size
    }
