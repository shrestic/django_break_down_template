import redis


def get_redis_client():
    return redis.Redis(host="localhost", port=6379, db=0)


# Test
if __name__ == "__main__":
    r = get_redis_client()
    r.set("key1", "hello")
    value = r.get("key1")
    print(f"Value: {value.decode('utf-8')}")
