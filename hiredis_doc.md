# hiredis_doc

## Giới thiệu
`hiredis` là một parser C nhanh cho giao thức Redis, được tích hợp với `redis-py` để tăng tốc độ phân tích dữ liệu từ Redis. Nó không phải thư viện độc lập mà là một optional dependency của `redis-py`. Khi cài `redis[hiredis]`, `redis-py` sẽ tự động dùng `hiredis` nếu có, cải thiện hiệu suất khi xử lý phản hồi lớn.

- **Phiên bản**: 3.1.0
- **Mục đích**: Tăng tốc độ parse dữ liệu từ Redis trong Python.
- **Link**: [https://github.com/redis/hiredis](https://github.com/redis/hiredis)
- **Yêu cầu**: Dùng với `redis-py` (`pip install redis[hiredis]`).

## Tác dụng
- **Tăng hiệu suất**: Parse dữ liệu nhanh hơn so với parser Python mặc định của `redis-py`.
- **Tối ưu API**: Không cần thay đổi code, chỉ cần cài `hiredis`.

## Ứng dụng thực tế
- Dùng trong API xử lý khối lượng dữ liệu lớn từ Redis.
- Tối ưu hệ thống cache hoặc pub/sub với nhiều truy vấn.

## Đặc điểm nổi bật
- **Nhẹ và nhanh**: Viết bằng C, hiệu suất cao hơn Python thuần.
- **Tích hợp tự động**: `redis-py` 5.2.1 tự nhận diện `hiredis` nếu cài.

---

## Ví dụ (Commits trong nhánh `hiredis`)

### Commit 1: So sánh hiệu suất cơ bản (sửa lỗi)
**Mô tả**: So sánh tốc độ GET với và không có `hiredis` bằng cách cài đặt riêng biệt.

#### Vị trí: `myapp/utils.py`
```python
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