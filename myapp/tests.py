from django.test import TestCase, Client
from myapp.models import Product
from django.urls import path
from myapp.views import product_list

urlpatterns = [
    path("products/", product_list, name="product-list"),
]


class ProductListViewTest(TestCase):
    def setUp(self):
        # Mock dữ liệu mẫu
        Product.objects.create(name="iPhone", price=999.99)
        Product.objects.create(name="MacBook", price=1999.99)

    def test_product_list_view(self):
        client = Client()
        response = client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["name"], "iPhone")
