
---

# 📘 `uvicorn_doc`

## 🚀 Giới thiệu  
**`uvicorn`** là một **ASGI (Asynchronous Server Gateway Interface)** web server dành cho Python, được tối ưu hóa cho các ứng dụng bất đồng bộ hiệu suất cao. Trong các dự án REST API sử dụng **Django REST Framework (DRF)**, `uvicorn` có thể chạy độc lập hoặc kết hợp với **Gunicorn** trong môi trường production.

- **Phiên bản khuyến nghị**: `uvicorn[standard]` `== 0.34.0`  
- **Mục tiêu sử dụng**:  
  - Chạy ứng dụng ASGI nhanh chóng, hỗ trợ `HTTP/1.1` và `WebSockets`
  - Tương thích tốt với FastAPI, Starlette, Django-ASGI  
- **Trang chủ**: [https://github.com/encode/uvicorn](https://github.com/encode/uvicorn)
- **Yêu cầu hệ thống**:
  - Python `>= 3.8`
  - Redis server nếu cần cache (Docker: `docker run -p 6379:6379 -d redis`)

---

## 🎯 Tác dụng chính
- ⚡ **Hiệu suất cao**: Tích hợp `uvloop` + `httptools` giúp tăng tốc xử lý.
- 🔁 **Tự động reload**: Hỗ trợ `--reload` khi phát triển.
- 🌐 **WebSockets ready**: Dễ dàng tích hợp kết nối thời gian thực.

---

## 📌 Ứng dụng thực tế
- Chạy REST API bất đồng bộ (FastAPI, DRF-ASGI).
- Dùng cho phát triển hoặc triển khai production (kết hợp Gunicorn).
- Tăng tốc độ khởi chạy và phản hồi của server.

---

## ✨ Đặc điểm nổi bật
| Tính năng                     | Mô tả                                                                 |
|-----------------------------|----------------------------------------------------------------------|
| ASGI Support                 | Tương thích hoàn toàn với các framework async như FastAPI, Starlette |
| `[standard]` Extras         | Cài thêm `uvloop`, `httptools`, `watchfiles`, `websockets`, v.v.    |
| Dễ sử dụng                  | Cài đặt đơn giản, CLI trực quan                                     |

---

## 🧪 Ví dụ sử dụng (Commit tương ứng trong branch `uvicorn`)

### ✅ Commit 1: Chạy Django REST Framework với Uvicorn
**Mô tả**: Khởi chạy một ứng dụng DRF thông qua Uvicorn (ASGI mode).

```bash
# Tạo project nếu chưa có
python manage.py runserver  # Kiểm tra project đã hoạt động

# Chạy bằng Uvicorn
uvicorn mainkode_example.asgi:application --host 0.0.0.0 --port 8000
```

**Test endpoint:**
```bash
curl http://127.0.0.1:8000/api/hello/
```

---

### 🔁 Commit 2: Dùng `--reload` khi phát triển
**Mô tả**: Chạy Uvicorn với chế độ auto-reload để tiện debug.

```bash
uvicorn mainkode_example.asgi:application --host 0.0.0.0 --port 8000 --reload
```

**Test thay đổi trực tiếp:**
1. Truy cập: [http://127.0.0.1:8000/api/hello/](http://127.0.0.1:8000/api/hello/)
2. Sửa `views.py`:
```python
return Response({"message": "Hi from DRF with Uvicorn!"})
```
3. Refresh trình duyệt.

**Kết quả**:
- Server reload tự động nhờ `watchfiles`
- Response thay đổi hiển thị ngay:  
  `{"message": "Hi from DRF with Uvicorn!"}`

---

### 📡 Commit 3: Tích hợp WebSocket
**Mô tả**: Cấu hình DRF để hỗ trợ WebSocket thông qua Uvicorn.

#### 1️⃣ `myapp/consumers.py`
```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"message": f"Echo: {text_data}"}))
```

#### 2️⃣ `myapp/routing.py`
```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]
```

#### 3️⃣ `mainkode_example/asgi.py` (cập nhật)
```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainkode_example.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
```

#### 4️⃣ Cài đặt thêm:
```bash
pip install channels
```

#### 5️⃣ Chạy server:
```bash
uvicorn mainkode_example.asgi:application --host 0.0.0.0 --port 8000
```

#### 6️⃣ Test bằng WebSocket client (ví dụ: `wscat`)
```bash
wscat -c ws://127.0.0.1:8000/ws/chat/
# Gõ: Hello
# Kết quả: {"message": "Echo: Hello"}
```

**Kết quả**:
- WebSocket hoạt động hoàn chỉnh nhờ `Uvicorn` và `websockets` từ gói `[standard]`.