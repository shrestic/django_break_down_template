import redis
import json

def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_data(key, value, timeout=60):
    r = get_redis_client()
    r.setex(key, timeout, json.dumps(value))

def get_cached_data(key):
    r = get_redis_client()
    data = r.get(key)
    return json.loads(data) if data else None