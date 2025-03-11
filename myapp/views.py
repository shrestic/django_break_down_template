from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class CacheTestView(APIView):
    def get(self, request):
        cache.set("test_key", "Hello Redis", timeout=60)
        value = cache.get("test_key")
        return Response({"value": value})


class ProductListView(APIView):
    def get(self, request):
        cache_key = "product_list"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        cache.set(cache_key, serializer.data, timeout=300)  # Cache 5 phút
        return Response(serializer.data)


class SessionTestView(APIView):
    def get(self, request):
        request.session["visit_count"] = request.session.get("visit_count", 0) + 1
        return Response({"visit_count": request.session["visit_count"]})
