Chào mày! Tao sẽ giải thích rõ về cơ chế default mà Django dùng khi tạo một project mới, đặc biệt liên quan đến việc reload server trong quá trình phát triển. Vì mày đang hỏi trong bối cảnh dùng `Werkzeug` với `watchdog`, tao sẽ kết nối nó với cách Django hoạt động mặc định để mày hiểu sâu hơn.

---

### Cơ chế default của Django khi tạo project mới

Khi mày tạo một project Django mới bằng lệnh:

```bash
django-admin startproject myproject
```

Django sẽ thiết lập một số thành phần mặc định, bao gồm server phát triển (development server). Cụ thể:

#### 1. **Development Server (runserver)**
- **Lệnh mặc định**: `python manage.py runserver`
- **Cơ chế reload**: Django dùng server phát triển dựa trên `wsgiref` (một WSGI server đơn giản trong Python standard library) kết hợp với một cơ chế reload.
- **Reload mặc định**: Sử dụng **polling** (giống `reloader_type='stat'` trong Werkzeug) để phát hiện thay đổi file.
  - **Cách hoạt động**: Mỗi giây, server quét tất cả file trong thư mục project (bao gồm `models.py`, `views.py`, `urls.py`, v.v.) bằng cách gọi `os.stat()` để kiểm tra thời gian sửa đổi (`mtime`). Nếu có file nào thay đổi, server tự động restart.
  - **Tùy chỉnh**: Mày có thể kiểm soát tần suất quét bằng `--reloader-interval` (mặc định là 1 giây).
- **Hiệu suất**: Với project nhỏ, polling hoạt động ổn, nhưng với project lớn (hàng nghìn file), nó có thể gây chậm trễ (1-2 giây) và tiêu tốn CPU.

#### 2. **Cấu hình WSGI**
- Django tạo file `myproject/wsgi.py` để định nghĩa ứng dụng WSGI. Khi chạy `runserver`, nó dùng file này để phục vụ request.
- Mặc định, không có `watchdog` được tích hợp, mà chỉ dùng polling đơn giản qua `wsgiref`.

#### 3. **Debugger**
- Khi chạy `runserver` với `--debug=True` (mặc định nếu `DEBUG = True` trong `settings.py`), Django cung cấp một trình debug cơ bản trong terminal, nhưng không có giao diện web tương tác như Werkzeug.

#### 4. **Không dùng Watchdog mặc định**
- Django không tích hợp `watchdog` theo mặc định khi tạo project. Để dùng `watchdog`, mày cần cài thư viện `watchdog` (hoặc thông qua `werkzeug[watchdog]` như mày đang làm) và cấu hình thủ công hoặc dùng server khác (như Werkzeug).

---

### So sánh với Werkzeug và Watchdog
- **Django default (`runserver`)**:
  - Dùng polling (`stat`) với interval 1 giây.
  - Không cần cài thêm thư viện, nhưng hiệu suất thấp hơn với project lớn.
  - Output ví dụ: `Watching for file changes with StatReloader`.

- **Werkzeug với `[watchdog]`**:
  - Dùng `watchdog` (nếu cài `werkzeug[watchdog]`) để theo dõi sự kiện file system (event-based).
  - Nhanh hơn, tiết kiệm tài nguyên, nhưng cần cài thêm `watchdog`.
  - Output ví dụ: `Restarting with watchdog (fsevents)` (trên macOS).

### Tại sao Django không dùng Watchdog mặc định?
1. **Đơn giản và nhẹ**: Polling hoạt động ổn với hầu hết project nhỏ/mới, không cần phụ thuộc thư viện bên ngoài.
2. **Tương thích**: Polling hoạt động trên mọi hệ điều hành mà không cần API đặc biệt (như `inotify` hay `fsevents`).
3. **Kích thước thư viện**: Giữ Django core nhẹ, để dev tự chọn thư viện nâng cao như `watchdog` nếu cần.

