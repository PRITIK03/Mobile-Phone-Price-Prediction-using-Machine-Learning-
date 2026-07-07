import hashlib
from datetime import datetime, timedelta
import io
import os
import json

# Try to initialize Redis if available and REDIS_URL is set
_use_redis = False
_redis_client = None
REDIS_URL = os.environ.get('REDIS_URL')
if REDIS_URL:
    try:
        import redis
        _redis_client = redis.from_url(REDIS_URL)
        # test connection
        _redis_client.ping()
        _use_redis = True
    except Exception:
        _use_redis = False

# In-memory fallback
prediction_cache = {}


def get_cache_key(battery_size, brand_name, memory_size):
    """Generate cache key for predictions"""
    data = f"{battery_size}_{brand_name}_{memory_size}"
    return hashlib.md5(data.encode()).hexdigest()


def _now_ts():
    return datetime.utcnow().timestamp()


def get_cached_prediction(cache_key):
    """Get cached prediction if available (5 minute TTL)"""
    ttl_seconds = 5 * 60
    if _use_redis and _redis_client:
        try:
            raw = _redis_client.get(cache_key)
            if not raw:
                return None
            payload = json.loads(raw.decode('utf-8'))
            ts = payload.get('timestamp', 0)
            if _now_ts() - ts < ttl_seconds:
                return payload.get('prediction')
            else:
                _redis_client.delete(cache_key)
                return None
        except Exception:
            return None
    else:
        if cache_key in prediction_cache:
            cached_data = prediction_cache[cache_key]
            if datetime.utcnow().timestamp() - cached_data['timestamp'] < ttl_seconds:
                return cached_data['prediction']
        return None


def cache_prediction(cache_key, prediction):
    """Cache prediction result"""
    payload = {
        'prediction': prediction,
        'timestamp': _now_ts()
    }
    if _use_redis and _redis_client:
        try:
            _redis_client.set(cache_key, json.dumps(payload))
        except Exception:
            # fallback to in-memory
            prediction_cache[cache_key] = payload
    else:
        prediction_cache[cache_key] = payload


def mock_predict_single(battery_size, brand_name, memory_size):
    """Return a deterministic mock prediction when real models aren't available."""
    base = 200 + (battery_size * 0.5) + (memory_size * 20)
    lowest_price = max(100, base)
    highest_price = lowest_price * 1.25
    release_date = int(datetime.utcnow().timestamp())
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
