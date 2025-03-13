from django.db import models


class Product(models.Model):
    """
    Product model đại diện cho một sản phẩm trong hệ thống.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Trả về chuỗi đại diện cho đối tượng Product.
        """
        return f"{self.name} - ${self.price}"
