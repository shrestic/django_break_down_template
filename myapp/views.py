from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='max_price',
                type=float,
                location=OpenApiParameter.QUERY,
                description='Filter products by maximum price'
            ),
        ],
        description='List all products, optionally filtered by max price.',
    )
    def list(self, request, *args, **kwargs):
        max_price = request.query_params.get('max_price')
        queryset = self.get_queryset()
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)