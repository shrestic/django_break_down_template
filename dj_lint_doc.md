### 📂 Branch: `pip-djlint-1.36.4`

---

### ✅ **Commit 1: Cài đặt `djlint==1.36.4`**
```bash
pip install djlint==1.36.4
```

**Giải thích:**
- [`djlint`](https://github.com/Riverside-Healthcare/djLint) là tool chuyên để:
  - **Format code HTML/Jinja/Django template**
  - **Lint các template Django** (cái mà `black`, `ruff`, `flake8` không chạm tới)
  - Phát hiện lỗi thụt dòng, block chưa đóng, style lộn xộn...
- Dùng rất ổn trong Django project để giữ template sạch, nhất quán.

---

### ✅ **Commit 2: Dùng `djlint` để lint toàn bộ template**
Giả sử trong Django project `mainkode_example`, mày có templates nằm ở:
```
mainkode_example/templates/
```

Thì chạy:
```bash
djlint mainkode_example/templates/
```

📌 DjLint sẽ tự động quét tất cả file `.html` trong đó và báo lỗi cú pháp, thụt dòng, block chưa đóng, v.v.

---

### ✅ **Commit 3: Tự động format template**
```bash
djlint mainkode_example/templates/ --reformat
```

📌 Format lại toàn bộ template giống như `black` làm với Python code.

Ví dụ template cũ:
```html
{% block content %}<h1>{{ title }}</h1>{%endblock%}
```

Sau khi format:
```html
{% block content %}
  <h1>{{ title }}</h1>
{% endblock %}
```

---

### ✅ **Commit 4: Kiểm tra lỗi nghiêm ngặt hơn**
```bash
djlint mainkode_example/templates/ --lint
```

Lúc này djLint sẽ:
- Báo lỗi block không đóng
- Tag không đúng vị trí
- Sử dụng indent chưa chuẩn
- Và một số custom rules khác

---

### ✅ **Commit 5: Optional – Cấu hình `djlint` trong `pyproject.toml`**

```toml
[tool.djlint]
profile = "django"
indent = 2
ignore = "H017,H030"  # nếu muốn bỏ qua một số rule
```

→ Dễ tích hợp hơn vào CI hoặc dùng chung team.

---

### ✅ **Commit 6: Tích hợp với `pre-commit`**
Tạo `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/Riverside-Healthcare/djlint
    rev: v1.36.4
    hooks:
      - id: djlint
        args: [--reformat]
```

Cài đặt:
```bash
pre-commit install
```

→ Tự reformat template mỗi lần commit.

---

### 📄 `pip-djlint-1.36.4_doc.md`

```markdown
# PIP: djlint==1.36.4

## 1. Cài đặt
```bash
pip install djlint==1.36.4
```

## 2. Mục đích
- Format và lint Django templates (`.html`)
- Phát hiện lỗi syntax, block hở, indent xấu...
- Giữ template sạch đẹp như `black` giữ code Python

## 3. Sử dụng

### Kiểm tra toàn bộ template
```bash
djlint mainkode_example/templates/
```

### Tự động format template
```bash
djlint mainkode_example/templates/ --reformat
```

### Báo lỗi nghiêm ngặt (strict)
```bash
djlint mainkode_example/templates/ --lint
```

## 4. Cấu hình (optional)
```toml
[tool.djlint]
profile = "django"
indent = 2
ignore = "H017,H030"
```

## 5. Pre-commit hook
```yaml
repos:
  - repo: https://github.com/Riverside-Healthcare/djlint
    rev: v1.36.4
    hooks:
      - id: djlint
        args: [--reformat]
```

```bash
pip install pre-commit
pre-commit install
```

## 6. Kết luận
- djlint giúp project Django đẹp, gọn, rõ.
- Đặc biệt phù hợp team đông người hoặc CI/CD cần enforce template style.
```
