from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .serializers import OrderSerializer
from .models import Order


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PendingOrderListView(generics.ListAPIView):
    queryset = Order.pending_orders.all()
    serializer_class = OrderSerializer
