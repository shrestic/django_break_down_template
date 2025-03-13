---

### ✅ **Commit 1: Cài đặt `ruff==0.9.10`**
```bash
pip install ruff==0.9.10
```

**Giải thích:**
- [`ruff`](https://github.com/astral-sh/ruff) là một **linter + formatter siêu nhanh**, thay thế cho `flake8`, `isort`, `pycodestyle`, `mccabe`, v.v.
- Viết bằng Rust → **tốc độ rất nhanh**, đặc biệt với project Django nhiều file.
- Phiên bản `0.9.10` vẫn hoạt động tốt, chỉ khác chút ở cú pháp CLI (dùng `check` thay vì gọi trực tiếp folder).

---

### ✅ **Commit 2: Kiểm tra code thủ công**
```bash
ruff check myapp/
```

**Giải thích:**
- Lệnh `check` là cách đúng để quét code với version `0.9.10`.
- Ruff sẽ báo tất cả các vi phạm theo PEP8, unused import, order import, missing blank lines, v.v.

📌 Ví dụ output:
```
myapp/views.py:1:1: F401 `json` imported but unused
myapp/models.py:3:5: E302 expected 2 blank lines, found 1
```

---

### ✅ **Commit 3: Tự động sửa lỗi code**
```bash
ruff check myapp/ --fix
```

- `--fix`: Cho phép Ruff tự động sửa những lỗi có thể fix được như unused import, import sort, extra blank lines…

---

### ✅ **Commit 4: Cấu hình `pyproject.toml` chuẩn**
Tạo file `pyproject.toml` ở root project:
```toml
[tool.ruff]
line-length = 88
exclude = ["migrations", "venv"]
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]  # bỏ rule dòng quá dài nếu thích
```

**Giải thích:**
- `select`: E (pycodestyle), F (pyflakes), I (isort)
- `ignore`: Bỏ rule `E501` nếu muốn viết dài hơn 88 ký tự (phối hợp với `black`)
- `target-version`: Cấu hình cho đúng version Python project đang dùng

---

### ✅ **Commit 5: Tích hợp `ruff` vào Git Hook với Pre-commit**

Tạo `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10
    hooks:
      - id: ruff
        args: ["check", "--fix"]
```

Cài đặt pre-commit:
```bash
pip install pre-commit
pre-commit install
```

Từ giờ mỗi lần `git commit`, `ruff` sẽ tự check code và fix lỗi trước khi commit được push.

---

### 📄 `pip-ruff-0.9.10_doc.md`

```markdown
# PIP: ruff==0.9.10

## 1. Cài đặt
```bash
pip install ruff==0.9.10
```

## 2. Mục đích
- Linter/Formatter hiệu suất cao thay cho flake8, isort, pycodestyle...
- Tự động fix lỗi nhanh chóng.
- Hữu ích cho dự án Django/Python lớn.

## 3. Cách dùng (CLI cho ruff==0.9.10)
```bash
ruff check myapp/
ruff check myapp/ --fix
```

## 4. Cấu hình `pyproject.toml`
```toml
[tool.ruff]
line-length = 88
exclude = ["migrations", "venv"]
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]
```

## 5. Pre-commit hook
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10
    hooks:
      - id: ruff
        args: ["check", "--fix"]
```

```bash
pip install pre-commit
pre-commit install
```

## 6. Kết luận
- `ruff` nên là công cụ mặc định cho mọi Python project.
- Có thể kết hợp thêm `black` nếu cần full-format theo style cứng hơn.
```