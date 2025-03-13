### ✅ **Commit 7: Thêm docstring chuẩn trong model và view `myapp`**

#### 🔸 `myapp/models.py`
```python
from django.db import models

class Product(models.Model):
    """
    Product model đại diện cho một sản phẩm trong hệ thống.

    Attributes:
        name (CharField): Tên sản phẩm.
        price (DecimalField): Giá sản phẩm.
        created_at (DateTimeField): Thời điểm tạo sản phẩm.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Trả về chuỗi đại diện cho đối tượng Product.
        """
        return f"{self.name} - ${self.price}"
```

---

#### 🔸 `myapp/views.py`
```python
from django.http import JsonResponse
from .models import Product

def product_list(request):
    """
    Trả về danh sách các sản phẩm dưới dạng JSON.

    Args:
        request (HttpRequest): Request từ client.

    Returns:
        JsonResponse: Danh sách sản phẩm dưới dạng JSON.
    """
    products = Product.objects.all().values("name", "price")
    return JsonResponse(list(products), safe=False)
```

---

### ✅ **Commit 8: Re-build tài liệu để hiển thị Docstring**
```bash
cd docs
make clean && make html
```

**Kết quả:** Trong file `docs/build/html/myapp.html`, phần mô tả `Product` và `product_list` sẽ được tự động generate từ các docstring vừa viết.

---

### 📄 Update file `pip-sphinx-django_doc.md`

```markdown
## 8. Viết docstring cho models và views

### `myapp/models.py`
```python
class Product(models.Model):
    """
    Product model đại diện cho một sản phẩm trong hệ thống.

    Attributes:
        name (CharField): Tên sản phẩm.
        price (DecimalField): Giá sản phẩm.
        created_at (DateTimeField): Thời điểm tạo sản phẩm.
    """
    ...
```

### `myapp/views.py`
```python
def product_list(request):
    """
    Trả về danh sách các sản phẩm dưới dạng JSON.

    Args:
        request (HttpRequest): Request từ client.
    Returns:
        JsonResponse: Danh sách sản phẩm dưới dạng JSON.
    """
```

## 9. Build lại tài liệu
```bash
cd docs
make clean && make html
```

## 10. Kết quả
Sphinx sẽ tự động hiển thị mô tả từ docstring trong file tài liệu HTML.
```
