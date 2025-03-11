from django.urls import path
from .views import BigListView

urlpatterns = [
    path("big-list/", BigListView.as_view(), name="big-list"),
]
