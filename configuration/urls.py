from django.contrib import admin
from django.urls import path, include
from configuration.views import HealthCheck

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health-check/", HealthCheck.as_view(), name="health-check"),
    path("api/products/", include("apps_dir.product.urls")),
]
