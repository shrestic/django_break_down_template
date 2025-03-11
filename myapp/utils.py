import redis
import time

def get_redis_client():
    # Không truyền parser_class, để redis-py tự động chọn dựa trên môi trường cài đặt
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Test hiệu suất
if __name__ == "__main__":
    r = get_redis_client()
    
    # Set dữ liệu lớn
    r.set('test_key', 'x' * 10000)
    
    # Đo thời gian không có hiredis (giả lập bằng cách chạy trước khi cài hiredis)
    print("Run this first without hiredis: pip install redis==5.2.1")
    start = time.time()
    for _ in range(1000):
        r.get('test_key')
    print(f"No hiredis: {time.time() - start:.4f}s")
    
    print("Then run again with hiredis: pip install redis[hiredis]")