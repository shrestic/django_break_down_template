# uvicorn_doc

## Giới thiệu
`uvicorn` là một ASGI (Asynchronous Server Gateway Interface) web server cho Python, được thiết kế để chạy các ứng dụng bất đồng bộ (async) hiệu suất cao. Trong bối cảnh REST API với Django (DRF), nó có thể được dùng để chạy các ứng dụng ASGI hoặc tích hợp với Gunicorn để triển khai production.

- **Phiên bản**: 0.34.0 (với `[standard]` extras)
- **Mục đích**: Chạy ứng dụng ASGI nhanh, hỗ trợ HTTP/1.1 và WebSockets.
- **Link**: [https://github.com/encode/uvicorn](https://github.com/encode/uvicorn)
- **Yêu cầu**: Python 3.8+, Redis server nếu cần cache (Docker: `docker run -p 6379:6379 -d redis`).

## Tác dụng
- **Hiệu suất cao**: Dùng `uvloop` và `httptools` (nếu cài `[standard]`) để tối ưu tốc độ.
- **Reload tự động**: Hỗ trợ `--reload` cho phát triển.
- **WebSockets**: Hỗ trợ kết nối thời gian thực.

## Ứng dụng thực tế
- Chạy API REST bất đồng bộ (như FastAPI hoặc DRF với ASGI).
- Triển khai production với Gunicorn.
- Phát triển nhanh với auto-reload.

## Đặc điểm nổi bật
- **ASGI**: Tương thích với các framework async như FastAPI, Starlette.
- **Extras `[standard]`**: Bao gồm `uvloop`, `httptools`, `websockets`, `watchfiles`, v.v.
- **Dễ dùng**: Cài đặt và chạy đơn giản qua CLI.

---

## Ví dụ (Commits trong nhánh `uvicorn`)

### Commit 1: Chạy DRF cơ bản với Uvicorn
**Mô tả**: Chạy một ứng dụng DRF đơn giản bằng Uvicorn.
*** Run
```
python manage.py runserver  # Tạo project nếu chưa có
uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000
```

*** Test
```
curl http://127.0.0.1:8000/api/hello/
```

#### Vị trí: `myapp/views.py`
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello from DRF with Uvicorn!"})