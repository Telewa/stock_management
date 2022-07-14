from django.contrib import admin

from apps_dir.product.models import Product


@admin.register(Product)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-updated_at",
        "-created_at",
        "id",
    )
    search_fields = ("name",)
