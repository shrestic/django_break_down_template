from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response


class CacheTestView(APIView):
    def get(self, request):
        cache.set("test_key", "Hello Redis", timeout=60)
        value = cache.get("test_key")
        return Response({"value": value})
