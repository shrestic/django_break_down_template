from rest_framework import serializers
from .models import Product
from .models import Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "created", "modified"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer_name", "status", "created", "modified"]
