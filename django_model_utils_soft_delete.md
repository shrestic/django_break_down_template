
### **Tóm tắt vấn đề**
Issue này được mở bởi `@danielquinn` trên GitHub, liên quan đến tính năng `SoftDeletableModel` trong thư viện `django-model-utils`. `SoftDeletableModel` là một lớp model hỗ trợ "xóa mềm" (soft delete), tức là thay vì xóa dữ liệu khỏi cơ sở dữ liệu, nó chỉ đánh dấu bản ghi là "đã xóa" (thường qua một trường như `is_deleted=True`) và ẩn chúng khỏi các truy vấn mặc định. Tuy nhiên, tác giả cho rằng cách triển khai hiện tại của tính năng này là một **anti-pattern** (mô hình thiết kế xấu) vì nó gây ra nhiều vấn đề nghiêm trọng trong ứng dụng Django.

---

### **Vấn đề cụ thể**
#### **1. Cách hoạt động của `SoftDeletableModel`**
- `SoftDeletableModel` ghi đè (override) manager mặc định `.objects` của Django để chỉ trả về các bản ghi chưa bị "xóa mềm" (tức là `is_deleted=False`).
- Điều này có nghĩa là khi bạn gọi `User.objects.all()`, bạn sẽ không thực sự nhận được **tất cả** bản ghi trong bảng `User`, mà chỉ nhận được những bản ghi chưa bị đánh dấu là xóa. Đây là sự thay đổi hành vi mặc định của Django, vốn thường trả về toàn bộ dữ liệu.

#### **2. Ví dụ minh họa vấn đề**
Tác giả đưa ra một ví dụ cụ thể:
```python
class User(SoftDeletableModel):
    name = models.CharField(max_length=128)

class Purchase(models.Model):
    user = models.ForeignKey(User)
    note = models.TextField()
```
- **Tình huống**:
  1. Tạo một `User` và một `Purchase` liên kết với user đó.
  2. "Xóa mềm" user bằng cách đánh dấu `is_deleted=True`.
  3. Vào Django Admin để chỉnh sửa trường `note` của `Purchase`.
- **Kết quả**: Django sẽ báo lỗi vì trường `user` trong `Purchase` tham chiếu đến một bản ghi không còn xuất hiện trong `User.objects.all()` (do đã bị "xóa mềm"). Tuy nhiên, bản ghi đó vẫn tồn tại trong cơ sở dữ liệu, dẫn đến sự mâu thuẫn và lỗi không mong muốn.

#### **3. Các vấn đề khác**
- **Debug khó khăn**: Một lập trình viên mới có thể dùng `User.objects.all().count()` để đếm số người dùng, nhưng kết quả sẽ không chính xác vì nó bỏ qua các bản ghi "xóa mềm". Điều này làm mất thời gian tìm lỗi.
- **Truy vấn phức tạp**: Khi thực hiện các truy vấn liên quan đến quan hệ (ví dụ: `Purchase.objects.filter(user__name__startswith="...")`), kết quả có thể không nhất quán hoặc gây lỗi vì `.objects` đã bị thay đổi hành vi.

#### **4. Tại sao đây là anti-pattern?**
- Việc ghi đè `.objects.all()` làm phá vỡ nguyên tắc **explicit is better than implicit** (rõ ràng tốt hơn ngầm định) của Python/Django. Người dùng mong đợi `.all()` trả về tất cả dữ liệu, nhưng thực tế lại không phải vậy.
- Gây ra lỗi khó lường trong các tính năng cốt lõi của Django, như Admin, hoặc trong các đoạn code phụ thuộc vào hành vi mặc định.

---

### **Đề xuất giải pháp**
Tác giả không phản đối ý tưởng "xóa mềm", mà chỉ không đồng ý với cách triển khai hiện tại. Ông đề xuất:
1. **Không ghi đè `.objects.all()`**:
   - Giữ nguyên `.objects` với hành vi mặc định của Django (trả về tất cả bản ghi, bất kể trạng thái xóa).
   - Thay vào đó, cung cấp một manager khác như `.available()` hoặc `.available_objects` để truy vấn các bản ghi chưa bị xóa mềm.
   - Ví dụ:
     ```python
     User.objects.all()  # Trả về tất cả, kể cả đã xóa mềm
     User.available()    # Chỉ trả về các bản ghi chưa xóa mềm
     ```

2. **Cảnh báo trong tài liệu**:
   - Nếu không thay đổi cách triển khai, ít nhất nên thêm một cảnh báo rõ ràng trong tài liệu của `django-model-utils` rằng việc dùng `SoftDeletableModel` có thể gây ra vấn đề về tính toàn vẹn dữ liệu và tương thích với các tính năng của Django (như Admin).

#### **Hậu quả của giải pháp**
- Thay đổi này sẽ phá vỡ các dự án hiện tại đang dùng `SoftDeletableModel` theo cách cũ, nhưng tác giả cho rằng lợi ích dài hạn (tránh lỗi và nhầm lẫn) quan trọng hơn.

---

### **Quan điểm cá nhân của tác giả**
- `@danielquinn` chia sẻ rằng ông đã gặp vấn đề này ở nhiều dự án khác nhau, mất hàng trăm giờ để sửa lỗi liên quan.
- Ông tin rằng cách triển khai hiện tại không chỉ không giải quyết tốt vấn đề "xóa mềm", mà còn tạo ra nhiều vấn đề mới, đặc biệt trong các dự án lớn hoặc khi chuyển giao cho lập trình viên khác.

---

### **Tóm lại**
Issue này không phải là lời chỉ trích cá nhân, mà là một phản hồi mang tính xây dựng về thiết kế của `SoftDeletableModel`. Tác giả lập luận rằng:
- Việc thay đổi hành vi mặc định của `.objects` là một ý tưởng tồi.
- Nên ưu tiên cách tiếp cận rõ ràng và không gây bất ngờ cho lập trình viên.
- Nếu không sửa, ít nhất cần cảnh báo người dùng về những rủi ro tiềm ẩn.