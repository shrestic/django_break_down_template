### 📂 Branch: `pip-pre-commit-4.1.0`

---

### ✅ **Commit 1: Cài đặt `pre-commit==4.1.0`**
```bash
pip install pre-commit==4.1.0
```

**Giải thích:**
- `pre-commit` là tool giúp kiểm tra và format code **trước khi commit vào Git**.
- Cực kỳ hiệu quả để enforce style code tự động trong team (không cần nhắc người khác “format code trước khi push” nữa).
- `pre-commit` sẽ chạy những tool như `black`, `ruff`, `djlint`, `flake8`, `isort`, v.v. **tự động trước commit**.

---

### ✅ **Commit 2: Khởi tạo config `.pre-commit-config.yaml`**

Tạo file `.pre-commit-config.yaml` ở root project `mainkode_example/`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10
    hooks:
      - id: ruff
        args: ["check", "--fix"]

  - repo: https://github.com/Riverside-Healthcare/djlint
    rev: v1.36.4
    hooks:
      - id: djlint
        args: ["--reformat"]
```

✅ Đây là ví dụ tích hợp `black`, `ruff`, `djlint` trong một pre-commit hook.

---

### ✅ **Commit 3: Cài đặt pre-commit vào Git hook**
```bash
pre-commit install
```

**Giải thích:**
- Câu lệnh này sẽ tạo `.git/hooks/pre-commit` và tự động chạy mỗi khi mày `git commit`.

---

### ✅ **Commit 4: Test thử pre-commit hoạt động**
- Tạo file `test.py`, viết 1 đoạn code sai style.
- Thử `git add test.py && git commit -m "test"`
- Pre-commit sẽ tự chạy `black`, `ruff`, `djlint` → sửa lỗi hoặc chặn commit nếu vi phạm.

---

### ✅ **Commit 5: Chạy thủ công pre-commit trên toàn bộ repo**
```bash
pre-commit run --all-files
```

→ Rất tiện để test toàn bộ codebase trước khi push.

---

### ✅ **Commit 6: (Optional) Tích hợp vào CI/CD hoặc yêu cầu threshold**

Cấu hình thêm `fail_fast: true`, enforce file types, hoặc thêm `skip: ["djlint"]` nếu cần bỏ từng hook riêng.

---

### 📄 `pip-pre-commit-4.1.0_doc.md`

```markdown
# PIP: pre-commit==4.1.0

## 1. Cài đặt
```bash
pip install pre-commit==4.1.0
```

## 2. Mục đích
- Tự động kiểm tra/lint/format code trước khi commit Git
- Tránh lỗi style code, import lộn xộn, HTML template xấu

## 3. Cấu hình `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10
    hooks:
      - id: ruff
        args: ["check", "--fix"]

  - repo: https://github.com/Riverside-Healthcare/djlint
    rev: v1.36.4
    hooks:
      - id: djlint
        args: ["--reformat"]
```

## 4. Cài hook Git
```bash
pre-commit install
```

## 5. Chạy manual toàn bộ repo
```bash
pre-commit run --all-files
```

## 6. Kết luận
- `pre-commit` là tool gần như **bắt buộc trong team dev chuyên nghiệp**
- Dễ tích hợp CI/CD
- Giúp clean code base mà không cần “soi” từng dòng khi review pull request
```
