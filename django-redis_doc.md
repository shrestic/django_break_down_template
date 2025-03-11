# django-redis_doc

## Giới thiệu
`django-redis` là một thư viện cung cấp backend cache dựa trên Redis cho Django, được thiết kế để tích hợp mượt mà với framework này. Nó xây dựng trên `redis-py`, bổ sung các tính năng đặc thù cho Django như cấu hình dễ dàng, hỗ trợ session, và các tùy chọn nâng cao (nén dữ liệu, sharding). Trong bối cảnh REST API với Django, nó rất hữu ích để tăng tốc ứng dụng bằng cách lưu trữ dữ liệu tạm thời.

- **Phiên bản**: Giả sử dùng bản mới nhất tương thích (ví dụ 5.4.0 tại thời điểm gần đây).
- **Mục đích**: Cung cấp cache backend mạnh mẽ cho Django, tận dụng Redis.
- **Link**: [https://github.com/jazzband/django-redis](https://github.com/jazzband/django-redis)
- **Yêu cầu**: Redis server chạy (Docker: `docker run -p 6379:6379 -d redis`), và `redis-py`.

## Tác dụng
- **Cache hiệu quả**: Lưu trữ dữ liệu tạm (kết quả API, trang render) để giảm tải database.
- **Session backend**: Dùng Redis để lưu phiên người dùng trong API.
- **Tùy chỉnh cao**: Hỗ trợ nén, sharding, và nhiều cấu hình Redis.

## Ứng dụng thực tế
- Cache kết quả API REST để trả về nhanh hơn.
- Lưu trữ session cho người dùng trong ứng dụng phân tán.
- Tăng hiệu suất cho các truy vấn nặng hoặc dữ liệu tĩnh.

## Đặc điểm nổi bật
- **Tích hợp Django**: Dùng trực tiếp với hệ thống cache của Django.
- **Hỗ trợ nén**: Giảm kích thước dữ liệu lưu trong Redis (gzip, lz4, zstd).
- **Pluggable client**: Tùy chỉnh Redis client nếu cần.

---

## Ví dụ (Commits trong nhánh `django-redis`)

### Commit 1: Cấu hình cơ bản và test cache
**Mô tả**: Cấu hình `django-redis` trong settings và thử SET/GET cơ bản.

#### Vị trí: `myproject/settings.py`
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Commit 3:
Trong lệnh:
```bash
curl -c cookies.txt -b cookies.txt http://127.0.0.1:8000/api/session-test/
```

### `cookies.txt` là file dùng để **lưu trữ cookie phiên làm việc** giữa các lần gửi request bằng `curl`.

Cụ thể:

| Tùy chọn `curl` | Ý nghĩa |
|-----------------|--------|
| `-c cookies.txt` | **"Save cookie vào file `cookies.txt"`** – tức là nếu server trả về cookie (như session ID), thì curl sẽ ghi lại vào file `cookies.txt`. |
| `-b cookies.txt` | **"Gửi cookie từ file `cookies.txt`"** – tức là curl sẽ đọc cookie từ file đó và gửi lại cho server (ví dụ: session cookie để duy trì đăng nhập). |

---

### Ví dụ thực tế:
Lần đầu gửi request:
```bash
curl -c cookies.txt http://127.0.0.1:8000/login/
```
→ Server trả về session cookie, curl sẽ lưu lại vào `cookies.txt`.

Lần sau:
```bash
curl -b cookies.txt http://127.0.0.1:8000/api/session-test/
```
→ curl sẽ gửi lại cookie đó để server biết bạn là **user đã login**, không bị coi là "khách lạ".

---