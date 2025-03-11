from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(
        request=ProductCreateSerializer,
        responses={201: ProductSerializer},
        examples=[
            OpenApiExample(
                "Valid creation example",
                value={"id": 1, "name": "Laptop", "price": "999.99", "description": "A high-end laptop"},
                response_only=True,
                status_codes=["201"],
            )
        ],
        description="Create a new product with name and price.",
    )
    def create(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = Product.objects.get(id=serializer.instance.id)
        return_serializer = ProductSerializer(instance)
        return Response(return_serializer.data, status=status.HTTP_201_CREATED)
