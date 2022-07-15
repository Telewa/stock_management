import csv
import io

from celery import shared_task, group
from django.db import transaction
from structlog import getLogger

from apps_dir.product.models import Product, Stock, Country

logger = getLogger(__file__)


@shared_task(bind=True, name="update_stock")
def update_stock(self, sku, product_name, country_code, stock_change):
    stock_change = int(stock_change)
    product, _ = Product.objects.get_or_create(
        sku=sku, defaults=dict(name=product_name)
    )
    country: Country = Country.objects.get(code=country_code.upper())

    with transaction.atomic():
        stock, created = Stock.objects.get_or_create(
            product=product, country=country, defaults={"number_of_items": stock_change}
        )
        if not created:
            stock.number_of_items += stock_change
            stock.save()


@shared_task(bind=True, name="get_items_for_stock_update")
def get_items_for_stock_update(self, decoded_file):
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)

    group(
        [
            update_stock.s(
                sku=row["sku"],
                product_name=row["name"],
                country_code=row["country"],
                stock_change=row["stock_change"],
            )
            for row in reader
        ]
    ).apply_async()
