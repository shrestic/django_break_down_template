from django.urls import path
from .views import ProductListView
from .views import OrderListView, PendingOrderListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/pending/", PendingOrderListView.as_view(), name="pending-orders"),
]
