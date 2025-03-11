---

### 1. `django==5.0.13`
- **Tác dụng**: Đây là framework chính - Django, nền tảng để xây dựng ứng dụng web bằng Python. Nó cung cấp mọi thứ từ routing, ORM (để làm việc với database), template engine, đến quản lý người dùng.
- **Ví dụ**: 
  - Tạo một trang web có URL `/blog/` để hiển thị danh sách bài viết từ database.
- **Ứng dụng**: Dùng để phát triển nhanh các ứng dụng web, từ blog cá nhân đến hệ thống quản lý doanh nghiệp lớn.
- **Đặc điểm nổi bật**: Nhanh, bảo mật, mở rộng tốt, đi kèm "batteries included" (nhiều tính năng sẵn có như admin, authentication).

---

### 2. `django-environ==0.12.0`
- **Tác dụng**: Giúp cấu hình ứng dụng Django bằng biến môi trường (environment variables), theo triết lý 12-factor app (một cách tiếp cận hiện đại để xây dựng ứng dụng).
- **Ví dụ**: 
  - File `.env`: `DEBUG=True` và `SECRET_KEY=abc123`
  - Code: `DEBUG = env('DEBUG')` để lấy giá trị từ `.env`.
- **Ứng dụng**: Quản lý cấu hình (như key bí mật, database URL) mà không hardcode trong code, phù hợp khi deploy lên nhiều môi trường (dev, staging, production).
- **Đặc điểm nổi bật**: Hỗ trợ parsing URL (như database connection string), dễ dùng, giảm rủi ro lộ thông tin nhạy cảm.

---

### 3. `django-model-utils==5.0.0`
- **Tác dụng**: Cung cấp các mixin và công cụ để làm việc với model trong Django dễ dàng hơn, như thêm trường tự động (timestamp), quản lý trạng thái, hoặc truy vấn phức tạp.
- **Ví dụ**: 
  - Dùng `TimeStampedModel` để tự động thêm `created_at` và `updated_at` vào model.
  ```python
  from model_utils.models import TimeStampedModel
  class Post(TimeStampedModel):
      title = models.CharField(max_length=100)
  ```
- **Ứng dụng**: Tiết kiệm thời gian khi định nghĩa model, đặc biệt với các tính năng phổ biến như theo dõi thời gian hoặc trạng thái.
- **Đặc điểm nổi bật**: Linh hoạt, tích hợp tốt với Django ORM, được cộng đồng Jazzband bảo trì.

---

### 4. `django-allauth[mfa]==65.4.1`
- **Tác dụng**: Thư viện toàn diện để xử lý xác thực (authentication) trong Django, bao gồm đăng nhập thông thường, đăng nhập bằng mạng xã hội (Google, Facebook), và quản lý tài khoản (đổi mật khẩu, xác minh email). Phần `[mfa]` thêm hỗ trợ xác thực hai yếu tố (2FA).
- **Ví dụ**: 
  - Đăng nhập bằng Google: Người dùng click nút "Login with Google" và được xác thực.
- **Ứng dụng**: Dùng trong các ứng dụng cần hệ thống đăng nhập mạnh mẽ, hỗ trợ cả local và social login, phổ biến trong e-commerce, SaaS.
- **Đặc điểm nổi bật**: Tích hợp sẵn nhiều provider (OAuth, OpenID), tùy chỉnh được, bảo mật cao với 2FA.

---

### 5. `django-crispy-forms==2.3`
- **Tác dụng**: Giúp render form trong Django đẹp và dễ tùy chỉnh mà không cần viết HTML thủ công, theo nguyên tắc DRY (Don't Repeat Yourself).
- **Ví dụ**: 
  ```python
  {% load crispy_forms_tags %}
  {% crispy form %}
  ```
  - Tạo form với layout đẹp (ví dụ: dùng Bootstrap) chỉ bằng vài dòng code.
- **Ứng dụng**: Dùng để tạo form đăng ký, đăng nhập, hoặc bất kỳ form nào trong giao diện web, tiết kiệm thời gian design.
- **Đặc điểm nổi bật**: Hỗ trợ nhiều framework UI (Bootstrap, Tailwind), dễ mở rộng.

---

### 6. `crispy-bootstrap5==2024.10`
- **Tác dụng**: Một gói mở rộng cho `django-crispy-forms`, thêm hỗ trợ template Bootstrap 5 để render form theo phong cách Bootstrap 5 (floating labels, accordion, switch).
- **Ví dụ**: 
  - Form với floating label: Nhãn tự động nổi lên khi nhập dữ liệu.
  ```python
  from crispy_bootstrap5.bootstrap5 import FloatingField
  layout = Layout(FloatingField("username"))
  ```
- **Ứng dụng**: Dùng khi muốn giao diện form hiện đại, phù hợp với Bootstrap 5 trong dự án Django.
- **Đặc điểm nổi bật**: Tận dụng các tính năng mới của Bootstrap 5, dễ tích hợp với `django-crispy-forms`.

---

### 7. `django-redis==5.4.0`
- **Tác dụng**: Cung cấp backend cache dùng Redis cho Django, giúp lưu trữ dữ liệu tạm thời để tăng tốc ứng dụng.
- **Ví dụ**: 
  - Lưu kết quả truy vấn database: `cache.set("top_posts", posts, timeout=3600)`
- **Ứng dụng**: Tăng hiệu suất web bằng cách cache trang, session, hoặc dữ liệu nặng, đặc biệt trong hệ thống lớn.
- **Đặc điểm nổi bật**: Hỗ trợ Redis đầy đủ (sharding, compression), tích hợp tốt với Django, có thể dùng làm session backend.

---

### 8. `djangorestframework==3.15.2`
- **Tác dụng**: Toolkit mạnh mẽ để xây dựng Web API trong Django, cung cấp các công cụ như serializer, viewset, router để tạo API RESTful.
- **Ví dụ**: 
  ```python
  class UserViewSet(viewsets.ModelViewSet):
      queryset = User.objects.all()
      serializer_class = UserSerializer
  ```
  - Tạo API `/users/` để lấy danh sách người dùng.
- **Ứng dụng**: Dùng để phát triển API cho ứng dụng web, mobile, hoặc SPA (Single Page Application).
- **Đặc điểm nổi bật**: Giao diện API browsable, dễ mở rộng, hỗ trợ authentication/permission.

---

### 9. `django-cors-headers==4.7.0`
- **Tác dụng**: Thêm header CORS (Cross-Origin Resource Sharing) vào response, cho phép ứng dụng Django giao tiếp với frontend từ domain khác.
- **Ví dụ**: 
  - Cấu hình: `CORS_ALLOWED_ORIGINS = ["https://frontend.com"]`
  - Cho phép frontend gọi API từ domain khác mà không bị chặn.
- **Ứng dụng**: Dùng khi backend và frontend chạy trên domain khác nhau (như API trên `api.example.com` và frontend trên `app.example.com`).
- **Đặc điểm nổi bật**: Dễ cấu hình, bảo mật tốt (chỉ cho phép origin cụ thể), hỗ trợ CSRF integration.

---

### 10. `drf-spectacular==0.28.0`
- **Tác dụng**: Tạo tài liệu OpenAPI (Swagger) cho API xây dựng bằng Django REST Framework, giúp mô tả chi tiết các endpoint.
- **Ví dụ**: 
  - Tự động tạo file `schema.yml` hoặc giao diện Swagger UI để xem tài liệu API.
  ```python
  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
  ```
- **Ứng dụng**: Tài liệu hóa API cho developer hoặc client, dễ dàng tích hợp với Swagger UI/Redoc.
- **Đặc điểm nổi bật**: Linh hoạt, tự động lấy thông tin từ DRF, hỗ trợ tùy chỉnh schema.

---

### Tổng kết
- **Framework chính**: `django` (nền tảng web).
- **Cấu hình**: `django-environ` (biến môi trường).
- **Model tiện ích**: `django-model-utils` (mở rộng model).
- **Xác thực**: `django-allauth` (login, social, 2FA).
- **Form**: `django-crispy-forms` + `crispy-bootstrap5` (render form đẹp).
- **Cache**: `django-redis` (tăng tốc ứng dụng).
- **API**: `djangorestframework` (xây dựng API), `django-cors-headers` (CORS), `drf-spectacular` (tài liệu API).