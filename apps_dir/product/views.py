from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from structlog import getLogger

from apps_dir.product.models import Product
from apps_dir.product.tasks import get_items_for_stock_update

logger = getLogger(__file__)


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ("file",)


class ProductView(APIView):
    def get(self, request, sku: str):
        """
        Get a product by SKU

        :param request:
        :param sku: str
        :return: Response
        """
        product_detail = None
        status_code = status.HTTP_200_OK

        try:
            product = Product.objects.get(sku=sku)
            product_detail = {"sku": product.sku, "name": product.name}
        except Product.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND

        return Response(status=status_code, data={"product": product_detail})

    def put(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]

        decoded_file = file.read().decode()
        get_items_for_stock_update.delay(decoded_file=decoded_file)

        return Response(status.HTTP_201_CREATED)
