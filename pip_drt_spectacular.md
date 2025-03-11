Chào mày! Tao sẽ làm vài ví dụ cơ bản về `drf-spectacular` để mày thấy cách nó hoạt động trong việc tạo tài liệu OpenAPI cho API xây dựng bằng Django REST Framework (DRF). Tao sẽ giữ mọi thứ đơn giản, dễ hiểu, và đi kèm code thực tế để mày có thể chạy thử luôn. Đây là các ví dụ từ cơ bản đến稍微 nâng cao một chút, tập trung vào cách tích hợp và tùy chỉnh.

---

### **Chuẩn bị**
Trước tiên, mày cần cài đặt môi trường với Django, DRF, và `drf-spectacular`. Tao giả sử mày đã có project Django sẵn, nếu chưa thì làm theo bước này:

1. Cài đặt:
   ```bash
   pip install django djangorestframework drf-spectacular
   ```

2. Thêm vào `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...,
       'rest_framework',
       'drf_spectacular',
   ]

   REST_FRAMEWORK = {
       'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
   }

   SPECTACULAR_SETTINGS = {
       'TITLE': 'My Awesome API',
       'DESCRIPTION': 'API for demo purposes',
       'VERSION': '1.0.0',
       'SERVE_INCLUDE_SCHEMA': False,  # Không phục vụ schema công khai
   }
   ```

3. Tạo một app (nếu chưa có):
   ```bash
   python manage.py startapp myapp
   ```

---

### **Ví dụ 1: Tạo schema cơ bản và xem qua Swagger UI**
Mục tiêu: Tạo một API đơn giản và dùng `drf-spectacular` để sinh schema, rồi xem qua giao diện Swagger.

#### Code
1. **Model** (`myapp/models.py`):
   ```python
   from django.db import models

   class Product(models.Model):
       name = models.CharField(max_length=100)
       price = models.DecimalField(max_digits=10, decimal_places=2)
       description = models.TextField()

       def __str__(self):
           return self.name
   ```

2. **Serializer** (`myapp/serializers.py`):
   ```python
   from rest_framework import serializers
   from .models import Product

   class ProductSerializer(serializers.ModelSerializer):
       class Meta:
           model = Product
           fields = ['id', 'name', 'price', 'description']
   ```

3. **View** (`myapp/views.py`):
   ```python
   from rest_framework import viewsets
   from .models import Product
   from .serializers import ProductSerializer

   class ProductViewSet(viewsets.ModelViewSet):
       queryset = Product.objects.all()
       serializer_class = ProductSerializer
   ```

4. **URL** (`myapp/urls.py`):
   ```python
   from django.urls import path, include
   from rest_framework.routers import DefaultRouter
   from .views import ProductViewSet
   from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

   router = DefaultRouter()
   router.register(r'products', ProductViewSet)

   urlpatterns = [
       path('', include(router.urls)),
       path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Endpoint để lấy schema
       path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
   ]
   ```

5. Thêm `myapp.urls` vào `urls.py` chính:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/', include('myapp.urls')),
   ]
   ```

6. Chạy migration và server:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

#### Kết quả
- Truy cập `http://127.0.0.1:8000/api/schema/swagger-ui/` để xem Swagger UI.
- Mày sẽ thấy danh sách các endpoint như `GET /api/products/`, `POST /api/products/`, v.v., với mô tả tự động về request/response dựa trên serializer.

---

### **Ví dụ 2: Tùy chỉnh schema với `@extend_schema`**
Mục tiêu: Thêm mô tả chi tiết và tham số tùy chỉnh cho một endpoint.

#### Code
1. Cập nhật `views.py`:
   ```python
   from rest_framework import viewsets
   from drf_spectacular.utils import extend_schema, OpenApiParameter
   from .models import Product
   from .serializers import ProductSerializer

   class ProductViewSet(viewsets.ModelViewSet):
       queryset = Product.objects.all()
       serializer_class = ProductSerializer

       @extend_schema(
           parameters=[
               OpenApiParameter(
                   name='max_price',
                   type=float,
                   location=OpenApiParameter.QUERY,
                   description='Filter products by maximum price'
               ),
           ],
           description='List all products, optionally filtered by max price.',
       )
       def list(self, request, *args, **kwargs):
           max_price = request.query_params.get('max_price')
           queryset = self.get_queryset()
           if max_price:
               queryset = queryset.filter(price__lte=max_price)
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)
   ```

#### Kết quả
- Trong Swagger UI, endpoint `GET /api/products/` sẽ hiển thị:
  - Mô tả: "List all products, optionally filtered by max price."
  - Tham số `max_price` trong phần query params, với kiểu `float`.
- Mày có thể thử gọi API: `http://127.0.0.1:8000/api/products/?max_price=50.0`.

---

### **Ví dụ 3: Tách request/response serializer và thêm ví dụ**
Mục tiêu: Dùng serializer khác nhau cho request và response, thêm ví dụ response.

#### Code
1. Thêm serializer mới (`myapp/serializers.py`):
   ```python
   from rest_framework import serializers
   from .models import Product

   class ProductCreateSerializer(serializers.ModelSerializer):
       class Meta:
           model = Product
           fields = ['name', 'price']  # Chỉ cần name và price khi tạo

   class ProductSerializer(serializers.ModelSerializer):
       class Meta:
           model = Product
           fields = ['id', 'name', 'price', 'description']
   ```

2. Cập nhật `views.py`:
   ```python
   from rest_framework import viewsets, status
   from rest_framework.response import Response
   from drf_spectacular.utils import extend_schema, OpenApiExample
   from .models import Product
   from .serializers import ProductSerializer, ProductCreateSerializer

   class ProductViewSet(viewsets.ModelViewSet):
       queryset = Product.objects.all()
       serializer_class = ProductSerializer

       @extend_schema(
           request=ProductCreateSerializer,
           responses={201: ProductSerializer},
           examples=[
               OpenApiExample(
                   'Valid creation example',
                   value={
                       'id': 1,
                       'name': 'Laptop',
                       'price': '999.99',
                       'description': 'A high-end laptop'
                   },
                   response_only=True,
                   status_codes=['201']
               )
           ],
           description='Create a new product with name and price.'
       )
       def create(self, request, *args, **kwargs):
           serializer = ProductCreateSerializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           self.perform_create(serializer)
           instance = Product.objects.get(id=serializer.instance.id)
           return_serializer = ProductSerializer(instance)
           return Response(return_serializer.data, status=status.HTTP_201_CREATED)
   ```

#### Kết quả
- Trong Swagger UI, endpoint `POST /api/products/`:
  - Request body chỉ yêu cầu `name` và `price`.
  - Response trả về đầy đủ `id`, `name`, `price`, `description`.
  - Có một ví dụ response hiển thị dưới dạng JSON như trong `OpenApiExample`.
- Thử gọi API: `curl -X POST -d '{"name": "Phone", "price": "499.99"}' -H "Content-Type: application/json" http://127.0.0.1:8000/api/products/`.

---

### **Ví dụ 4: Xuất schema ra file YAML**
Mục tiêu: Sinh file schema để dùng offline hoặc tích hợp với công cụ khác.

#### Code
1. Chạy lệnh CLI:
   ```bash
   python manage.py spectacular --file schema.yml --color
   ```

2. (Tùy chọn) Validate schema:
   ```bash
   python manage.py spectacular --file schema.yml --validate
   ```

#### Kết quả
- File `schema.yml` được tạo trong thư mục project, chứa toàn bộ mô tả API theo chuẩn OpenAPI.
- Mày có thể dùng file này với Swagger UI offline:
  ```bash
  docker run -p 80:8080 -e SWAGGER_JSON=/schema.yml -v $(pwd)/schema.yml:/schema.yml swaggerapi/swagger-ui
  ```
- Truy cập `http://localhost` để xem.

---

### **Lưu ý**
- **`@extend_schema`**: Là công cụ mạnh mẽ để tùy chỉnh schema, mày có thể thêm parameter, override description, hay thay đổi operation_id.
- **Tích hợp UI**: Ngoài Swagger, mày có thể dùng Redoc bằng cách thêm `SpectacularRedocView` vào `urls.py`.
- **Debug**: Nếu schema không như ý, kiểm tra serializer và view, vì `drf-spectacular` dựa vào chúng để suy ra schema.

Mày muốn thử cái nào sâu hơn hoặc cần thêm ví dụ cụ thể không? Bảo tao nhé!