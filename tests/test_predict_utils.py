import time
from predict_utils import get_cache_key, cache_prediction, get_cached_prediction, mock_predict_single, prediction_cache


def test_get_cache_key_unique():
    k1 = get_cache_key(100, 'Samsung', 64)
    k2 = get_cache_key(101, 'Samsung', 64)
    assert k1 != k2


def test_cache_and_get():
    key = get_cache_key(200, 'Xiaomi', 128)
    # ensure no existing
    if key in prediction_cache:
        del prediction_cache[key]
    res = {'a': 1}
    cache_prediction(key, res)
    got = get_cached_prediction(key)
    assert got == res


def test_cache_expiry():
    key = get_cache_key(300, 'OnePlus', 256)
    if key in prediction_cache:
        del prediction_cache[key]
    res = {'b': 2}
    cache_prediction(key, res)
    got = get_cached_prediction(key)
    assert got == res
    # simulate expiry by modifying timestamp directly (works for in-memory fallback)
    if key in prediction_cache:
        prediction_cache[key]['timestamp'] -= 60 * 10
    got2 = get_cached_prediction(key)
    assert got2 is None


def test_mock_predict_single():
    r = mock_predict_single(4000, 'Samsung', 128)
    assert 'model_name' in r
    assert 'lowest_price' in r
    assert 'highest_price' in r
    assert 'release_date' in r
    assert 'screen_size' in r
