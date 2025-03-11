from django.urls import path
from .views import ProductListView
from .views import OrderListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
]
