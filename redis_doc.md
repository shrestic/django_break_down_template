# redis_doc

## Giới thiệu
`redis` (redis-py) là thư viện Python chính thức để giao tiếp với Redis - một cơ sở dữ liệu key-value in-memory nhanh, thường dùng làm cache, hàng đợi, hoặc lưu trữ dữ liệu tạm thời. Trong REST API với Django, nó rất hữu ích để tăng tốc ứng dụng bằng cách lưu trữ dữ liệu tạm hoặc quản lý session.

- **Phiên bản**: 5.2.1
- **Mục đích**: Kết nối và thao tác với Redis từ Python.
- **Link**: [https://github.com/redis/redis-py](https://github.com/redis/redis-py)
- **Yêu cầu**: Redis server phải chạy (có thể dùng Docker: `docker run -p 6379:6379 redis`).

## Tác dụng
- **Cache dữ liệu**: Lưu trữ kết quả truy vấn hoặc dữ liệu tạm để giảm tải database.
- **Hàng đợi**: Quản lý tác vụ bất đồng bộ (dùng với Celery chẳng hạn).
- **Session**: Lưu trữ phiên người dùng trong API.

## Ứng dụng thực tế
- Cache kết quả API để trả về nhanh hơn.
- Lưu trữ trạng thái tạm thời (như token, counter).
- Dùng trong hệ thống phân tán để đồng bộ dữ liệu.

## Đặc điểm nổi bật
- **Hỗ trợ đầy đủ Redis**: Gần như tất cả lệnh Redis (SET, GET, HSET, etc.) đều có.
- **Connection Pool**: Quản lý kết nối hiệu quả, tránh tạo mới liên tục.
- **Hỗ trợ RESP3**: Giao thức mới của Redis (từ phiên bản 5.0).

---

## Ví dụ (Commits trong nhánh `redis`)

### Commit 1: Kết nối cơ bản và SET/GET
**Mô tả**: Kết nối Redis và thử SET/GET cơ bản, đặt trong `utils.py`.

#### Vị trí: `myapp/utils.py`
```python
import redis

def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)

# Test
if __name__ == "__main__":
    r = get_redis_client()
    r.set('key1', 'hello')
    value = r.get('key1')
    print(f"Value: {value.decode('utf-8')}")