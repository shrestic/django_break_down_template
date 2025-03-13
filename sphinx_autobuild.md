---

### ✅ **Commit 1: Cài đặt `sphinx-autobuild==2024.10.3`**
```bash
pip install sphinx-autobuild==2024.10.3
```

**Giải thích:**
- `sphinx-autobuild` là tool giúp mày **build tài liệu + tự động reload browser khi có thay đổi**, rất tiện như một "live-server" cho Sphinx.
- Tăng tốc quá trình viết và test docs cực kỳ hiệu quả, nhất là khi làm việc nhóm hoặc chỉnh sửa docs liên tục.

---

### ✅ **Commit 2: Sử dụng `sphinx-autobuild` để xem tài liệu trực tiếp**

Thay vì:
```bash
make html && open docs/build/html/index.html
```

Giờ chỉ cần:
```bash
sphinx-autobuild docs/source docs/build/html
```

- `docs/source`: nơi chứa file `.rst`, `conf.py`, v.v.
- `docs/build/html`: nơi Sphinx build HTML ra.
- Tool này sẽ **tự theo dõi thay đổi**, nếu mày sửa file `.rst`, `.py`, `.html`, `conf.py`... → tự rebuild lại docs và reload browser liền.

Sau khi chạy, terminal sẽ hiển thị:
```
Serving on http://127.0.0.1:8000
```

→ Mở trình duyệt vào đó để xem **Live Docs**.

---

### ✅ **Commit 3: Tích hợp vào `Makefile` cho tiện (optional)**

Mở file `docs/Makefile`, thêm vào cuối:
```makefile
autobuild:
	sphinx-autobuild source build/html
```

Giờ mày chỉ cần chạy:
```bash
make autobuild
```

→ Cũng sẽ bật live server giống hệt.

---

### 📄 `pip-sphinx-autobuild-2024.10.3_doc.md`

```markdown
# PIP: sphinx-autobuild==2024.10.3

## 1. Cài đặt
```bash
pip install sphinx-autobuild==2024.10.3
```

## 2. Mục đích
- Tự động rebuild docs khi có thay đổi `.rst`, `.py`, `conf.py`, v.v.
- Tự reload trình duyệt → xem live docs nhanh chóng.

## 3. Cách chạy
```bash
sphinx-autobuild docs/source docs/build/html
```

→ Truy cập tại http://127.0.0.1:8000

## 4. Optional: Thêm vào Makefile
```makefile
autobuild:
	sphinx-autobuild source build/html
```
Sau đó chỉ cần:
```bash
make autobuild
```

## 5. Kết luận
Dễ viết docs, dễ test, tiết kiệm thời gian build thủ công.
```