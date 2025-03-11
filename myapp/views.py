from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .utils import cache_data, get_cached_data

class ProductListView(APIView):
    def get(self, request):
        cache_key = 'product_list'
        cached = get_cached_data(cache_key)
        if cached:
            return Response(cached)
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        cache_data(cache_key, serializer.data)
        return Response(serializer.data)