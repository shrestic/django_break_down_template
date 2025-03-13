### ✅ **Commit 1: Cài thêm pytest + plugin Django**
```bash
pip install coverage==7.6.12 pytest pytest-django
```

---

### ✅ **Commit 2: Cấu hình `pytest` cho Django project**

Tạo file `pytest.ini` ở root project (`mainkode_example/`):
```ini
[pytest]
DJANGO_SETTINGS_MODULE = mainkode_example.settings
python_files = tests.py test_*.py *_tests.py
```

**Giải thích:**
- `DJANGO_SETTINGS_MODULE`: để pytest biết cần load config nào từ Django.
- `python_files`: quy tắc nhận diện file test.

---

### ✅ **Commit 3: Chạy coverage với pytest**

```bash
coverage run -m pytest
```

- `-m pytest`: coverage wrap lại lệnh pytest để đo coverage.

---

### ✅ **Commit 4: Xem kết quả như cũ**
```bash
coverage report
coverage html
```

Mọi thứ vẫn y chang như flow `manage.py test`.

---

### ✅ **Commit 5: Optional – Cấu hình ignore file `.coveragerc` vẫn giữ nguyên**
```ini
[run]
omit =
    */migrations/*
    */tests/*
    */settings/*
    */venv/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __str__
    if self\.debug
```

---

### ✅ **Commit 6: Ví dụ test vẫn dùng được y chang**
`myapp/tests/test_views.py` vẫn giữ nguyên. Không cần đổi gì cả, vì `pytest` vẫn chạy được `TestCase` của Django.

✔ Nhưng nếu mày muốn chơi **pure pytest style**, thì ví dụ mới đây:

```python
import pytest
from django.test import Client
from myapp.models import Product

@pytest.mark.django_db
def test_product_list_view():
    Product.objects.create(name="iPhone", price=999.99)
    Product.objects.create(name="MacBook", price=1999.99)

    client = Client()
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 2
```

---

### 📄 Update `pip-coverage-7.6.12_doc.md` thêm phần `pytest` style

```markdown
## 11. Dùng coverage + pytest thay manage.py test

### Cài thêm:
```bash
pip install pytest pytest-django
```

### Cấu hình pytest:
`pytest.ini`
```ini
[pytest]
DJANGO_SETTINGS_MODULE = mainkode_example.settings
python_files = tests.py test_*.py *_tests.py
```

### Chạy test + đo coverage
```bash
coverage run -m pytest
coverage report
coverage html
```

### Ví dụ test dạng pytest:
```python
import pytest
from django.test import Client
from myapp.models import Product

@pytest.mark.django_db
def test_product_list_view():
    Product.objects.create(name="iPhone", price=999.99)
    Product.objects.create(name="MacBook", price=1999.99)

    client = Client()
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 2
```
```

---

✅ Kết luận:
- `coverage run -m pytest` hoàn toàn thay thế được `coverage run manage.py test`.
- `pytest` gọn hơn, dễ viết test nâng cao hơn (`parametrize`, fixture, v.v.)
- Tùy phong cách code, mày chọn hướng nào cũng ổn.
