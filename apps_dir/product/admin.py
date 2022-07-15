from django.contrib import admin

from apps_dir.product.models import Product, Country, Stock


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "sku",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
        "created_at",
        "updated_at",
        "id",
    )
    search_fields = (
        "name",
        "sku",
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
        "code",
        "-created_at",
        "-updated_at",
        # "id",
    )
    search_fields = (
        "name",
        "code",
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "country",
        "number_of_items",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-updated_at",
        "-created_at",
        "id",
    )
    search_fields = (
        "product__sku",
        "product__name",
    )
    list_filter = ("country",)
