### 📂 Branch: `pip-factory-boy-3.3.2`

---

### ✅ **Commit 1: Cài đặt `factory-boy==3.3.2`**
```bash
pip install factory-boy==3.3.2
```

**Giải thích:**
- [`factory_boy`](https://factoryboy.readthedocs.io/) là một thư viện hỗ trợ tạo dữ liệu giả **(test data factories)** cho unit test.
- Được dùng thay thế cho cách tạo thủ công bằng `Model.objects.create(...)` trong `setUp()` hoặc `fixtures`.
- Rất phổ biến trong Django + pytest + coverage + CI/CD workflows.

---

### ✅ **Commit 2: Tạo factory cho model `Product` trong `myapp`**

Giả sử model của mày đã có:

📁 `myapp/models.py`
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
```

➡ Tạo factory tương ứng:

📁 `myapp/factories.py`
```python
import factory
from myapp.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
```

---

### ✅ **Commit 3: Dùng factory trong test để mock data**

📁 `myapp/tests/test_views.py`
```python
import pytest
from django.test import Client
from myapp.factories import ProductFactory

@pytest.mark.django_db
def test_product_list_view():
    ProductFactory.create_batch(5)  # Tạo 5 sản phẩm fake

    client = Client()
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 5
```

**Giải thích:**
- `create_batch(5)`: tạo nhanh 5 bản ghi.
- Factory dễ maintain hơn, dễ mở rộng khi có nhiều field.

---

### ✅ **Commit 4: Custom factory khi cần**
Mày cũng có thể tuỳ chỉnh factory khi cần tạo dữ liệu cụ thể:
```python
ProductFactory(name="MacBook Pro", price=2499.99)
```

---

### ✅ **Commit 5: Tạo nhiều factory cho các model khác**
Sau này nếu mày có thêm `UserFactory`, `OrderFactory`, `CategoryFactory`, chỉ cần tách file rõ ràng:
```
myapp/
├── factories/
│   ├── __init__.py
│   ├── product_factory.py
│   └── user_factory.py
```

---

### 📄 `pip-factory-boy-3.3.2_doc.md`

```markdown
# PIP: factory-boy==3.3.2

## 1. Cài đặt
```bash
pip install factory-boy==3.3.2
```

## 2. Mục đích
- Tạo mock/test data nhanh, sạch và tái sử dụng tốt
- Thay thế cách thủ công `Model.objects.create()` trong test

## 3. Tạo factory cho model `Product`

`myapp/factories.py`
```python
import factory
from myapp.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
```

## 4. Dùng trong test
```python
import pytest
from django.test import Client
from myapp.factories import ProductFactory

@pytest.mark.django_db
def test_product_list_view():
    ProductFactory.create_batch(5)
    client = Client()
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 5
```

## 5. Ghi nhớ
- `create()` tạo 1 bản ghi
- `create_batch(N)` tạo nhiều bản ghi
- Dễ custom field bất kỳ khi cần

## 6. Kết luận
- `factory_boy` là công cụ quan trọng khi viết test hiệu quả, nhanh, sạch.
- Phối hợp cực tốt với `pytest`, `coverage`, `pre-commit`, `CI/CD`.
```
