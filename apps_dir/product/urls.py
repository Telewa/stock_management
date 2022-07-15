from django.urls import path
from .views import ProductView

urlpatterns = [
    path("", ProductView.as_view(), name="products"),
    path("<str:sku>/", ProductView.as_view(), name="product"),
    path(
        "consume/<str:sku>/<str:country_code>",
        ProductView.as_view(),
        name="consume-product",
    ),
]
