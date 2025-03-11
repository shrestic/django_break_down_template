from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    STATUS = Choices(
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    )
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS.pending)
    customer_name = models.CharField(max_length=100)
