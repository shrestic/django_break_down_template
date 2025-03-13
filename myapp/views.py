from django.http import JsonResponse
from .models import Product


def product_list(request):
    """
    Trả về danh sách các sản phẩm dưới dạng JSON.

    Args:
        request (HttpRequest): Request từ client.

    Returns:
        JsonResponse: Danh sách sản phẩm dưới dạng JSON.
    """
    products = Product.objects.all().values("name", "price")
    return JsonResponse(list(products), safe=False)
