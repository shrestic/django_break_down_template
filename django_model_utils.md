# 📘 `django-model-utils_doc`

## 🚀 Giới thiệu  
**`django-model-utils`** là một thư viện mở rộng mạnh mẽ cho Django ORM, cung cấp các **mixin, manager và tiện ích bổ sung** giúp đơn giản hóa công việc với model. Trong dự án REST API với **Django REST Framework (DRF)**, thư viện này giúp bạn dễ dàng tích hợp các tính năng như **timestamp, trạng thái, soft delete, custom queryset** mà không cần viết thủ công.

- **Phiên bản khuyến nghị**: `django-model-utils==5.0.0`
- **Mục tiêu sử dụng**:
  - Tự động thêm trường `created`, `modified`
  - Quản lý trạng thái với `StatusModel`
  - Quản lý logic truy vấn nâng cao với `QueryManager`
  - Xóa mềm dữ liệu với `SoftDeletableModel`
- **Trang chủ**: [https://github.com/jazzband/django-model-utils](https://github.com/jazzband/django-model-utils)
- **Yêu cầu hệ thống**:
  - Django `>= 5.0`
  - DRF, PostgreSQL hoặc SQLite

---

## 🎯 Tác dụng chính
- ⏱️ **Tự động tracking thời gian tạo/cập nhật**
- 🔄 **Quản lý trạng thái dễ dàng qua `Choices`**
- 🔍 **Truy vấn nâng cao thông qua `QueryManager`**
- 🗑️ **Hỗ trợ xóa mềm (soft delete)**

---

## 📌 Ứng dụng thực tế
- Theo dõi log thời gian của bản ghi API.
- Quản lý trạng thái đơn hàng trong e-commerce.
- Lọc dữ liệu chủ động theo trạng thái hoặc điều kiện.
- Giữ dữ liệu an toàn nhờ soft delete thay vì hard delete.

---

## ✨ Đặc điểm nổi bật
| Tính năng               | Mô tả                                                           |
|------------------------|-----------------------------------------------------------------|
| `TimeStampedModel`     | Tự động thêm `created` và `modified` datetime fields            |
| `StatusModel` + Choices| Quản lý trạng thái rõ ràng, dễ sử dụng                          |
| `QueryManager`         | Định nghĩa các queryset theo trạng thái / điều kiện            |
| `SoftDeletableModel`   | Hỗ trợ xóa mềm (`is_deleted=True`) mà không mất dữ liệu         |

---

## 🧪 Ví dụ sử dụng (Commits tương ứng trong branch `django-model-utils`)

### ✅ Commit 1: Sử dụng `TimeStampedModel`
**Mô tả**: Tự động thêm `created` và `modified` vào model Product.

```python
# myapp/models.py
from django.db import models
from model_utils.models import TimeStampedModel

class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

```python
# myapp/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'created', 'modified']
```

```python
# myapp/views.py
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

```python
# myapp/urls.py
from django.urls import path
from .views import ProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
]
```

```bash
pip install django djangorestframework django-model-utils==5.0.0
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

**Test:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Laptop", "price": "999.99"}' http://127.0.0.1:8000/api/products/
curl http://127.0.0.1:8000/api/products/
```

---

### 🔁 Commit 2: Sử dụng `StatusModel` với `Choices`
**Mô tả**: Quản lý trạng thái đơn hàng bằng status field.

```python
# myapp/models.py
from model_utils.models import TimeStampedModel
from model_utils import Choices

class Order(TimeStampedModel):
    STATUS = Choices(
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS.pending)
    customer_name = models.CharField(max_length=100)
```

```python
# serializers/views/urls tương tự Commit 1, chỉ thay đổi model và serializer fields
```

**Test:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"customer_name": "Phong", "status": "pending"}' http://127.0.0.1:8000/api/orders/
curl http://127.0.0.1:8000/api/orders/
```

---

### 🔍 Commit 3: Dùng `QueryManager` cho filter theo trạng thái
**Mô tả**: Thêm manager để lọc đơn hàng `pending` và `delivered`.

```python
# myapp/models.py
from model_utils.managers import QueryManager

class Order(TimeStampedModel):
    ...
    objects = models.Manager()
    pending_orders = QueryManager(status=STATUS.pending)
    delivered_orders = QueryManager(status=STATUS.delivered)
```

```python
# myapp/views.py
class PendingOrderListView(generics.ListAPIView):
    queryset = Order.pending_orders.all()
    serializer_class = OrderSerializer
```

```python
# myapp/urls.py
urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/pending/', PendingOrderListView.as_view(), name='pending-orders'),
]
```

**Test:**
```bash
curl http://127.0.0.1:8000/api/orders/pending/
```

---

### 🗑️ Commit 4: Dùng `SoftDeletableModel` để xóa mềm
**Mô tả**: Thay vì xóa khỏi DB, đơn hàng sẽ được gắn `is_deleted=True`.

```python
# myapp/models.py
from model_utils.models import SoftDeletableModel

class Order(TimeStampedModel, SoftDeletableModel):
    ...
    active_objects = QueryManager(is_deleted=False)
```

```python
# views.py
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.active_objects.all()
    ...

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.active_objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
```

```python
# urls.py
urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDeleteView.as_view(), name='order-delete'),
]
```

**Test:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/orders/1/
curl http://127.0.0.1:8000/api/orders/
```

**Kết quả:**
- `Order.objects.all()` vẫn thấy bản ghi.
- `Order.active_objects.all()` không thấy bản ghi đã xóa mềm.

---

## 📁 Cấu trúc nhánh Git
```
Branch: django-model-utils
├── Commit 1: Add TimeStampedModel for Product model
├── Commit 2: Add StatusModel for Order with choices
├── Commit 3: Add QueryManager for filtering pending orders
└── Commit 4: Add SoftDeleteModel for soft deletion
```

---

## 📝 Ghi chú bổ sung
- `django-model-utils` giúp viết code model ngắn gọn hơn, DRY hơn.
- Dễ bảo trì và mở rộng hệ thống REST API với các tính năng phổ biến.
- Kết hợp tốt với DRF qua generic views và serializers.

