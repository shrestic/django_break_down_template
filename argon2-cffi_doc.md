# argon2-cffi_doc

## Giới thiệu
`argon2-cffi` là một thư viện Python cung cấp binding cho thuật toán băm mật khẩu Argon2 - một thuật toán hiện đại, an toàn, được thiết kế để chống lại các cuộc tấn công brute-force và side-channel. Trong bối cảnh REST API với Django, nó rất hữu ích để bảo mật mật khẩu người dùng khi lưu trữ qua endpoint đăng ký hoặc đăng nhập.

- **Phiên bản**: 23.1.0
- **Mục đích**: Băm mật khẩu an toàn và xác minh mật khẩu qua API.
- **Link**: [https://github.com/hynek/argon2-cffi](https://github.com/hynek/argon2-cffi)
- **Yêu cầu**: Cần `libargon2` trên hệ thống, nhưng pip sẽ tự xử lý.

## Tác dụng
- **Bảo mật mật khẩu**: Chuyển mật khẩu plaintext thành hash không thể đảo ngược.
- **Chống tấn công**: Dùng tài nguyên (memory, CPU) để làm chậm các cuộc tấn công.
- **Dễ tích hợp**: Hỗ trợ API REST qua DRF để đăng ký/đăng nhập.

## Ứng dụng thực tế
- Lưu trữ mật khẩu người dùng trong API đăng ký.
- Xác minh mật khẩu khi đăng nhập qua endpoint REST.
- Phù hợp với các hệ thống REST yêu cầu bảo mật cao.

## Đặc điểm nổi bật
- **Argon2**: Thuật toán tiên tiến, chống brute-force hiệu quả.
- **Ba biến thể**: Argon2i, Argon2d, Argon2id (mặc định là Argon2id).
- **Tích hợp DRF**: Dễ dùng với Django authentication trong API.

---

## Ví dụ (Commits trong nhánh `argon2-cffi`)

### Commit 1: Cài đặt và băm mật khẩu cơ bản
**Mô tả**: Ví dụ cơ bản băm mật khẩu, đặt trong một file utils để tái sử dụng trong API.

#### Vị trí: `myapp/utils.py`
```python
from argon2 import PasswordHasher

def hash_password(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)

# Test cơ bản
if __name__ == "__main__":
    password = "mypassword123"
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")