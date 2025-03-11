import redis
import json


def get_redis_client():
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def cache_data(key, value, timeout=60):
    r = get_redis_client()
    r.setex(key, timeout, json.dumps(value))


def get_cached_data(key):
    r = get_redis_client()
    data = r.get(key)
    return json.loads(data) if data else None


def batch_set_data(data_dict):
    r = get_redis_client()
    with r.pipeline() as pipe:
        for key, value in data_dict.items():
            pipe.set(key, json.dumps(value))
        pipe.execute()


if __name__ == "__main__":
    data = {"key1": "value1", "key2": "value2"}
    batch_set_data(data)
    r = get_redis_client()
    print(r.get("key1"), r.get("key2"))
