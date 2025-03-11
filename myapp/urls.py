from django.urls import path
from .views import CacheTestView

urlpatterns = [
    path('cache-test/', CacheTestView.as_view(), name='cache-test'),
]