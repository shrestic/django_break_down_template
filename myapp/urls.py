from django.urls import path
from .views import CacheTestView, ProductListView, SessionTestView

urlpatterns = [
    path('cache-test/', CacheTestView.as_view(), name='cache-test'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('session-test/', SessionTestView.as_view(), name='session-test'),
]