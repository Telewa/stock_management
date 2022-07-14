from django.db import models


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return super(CommonInfo, self).__str__()


class Product(CommonInfo):
    sku = models.CharField(
        max_length=150, unique=True, blank=False, null=False, db_index=True
    )
    name = models.CharField(max_length=150, blank=False, null=False)


class Stock(CommonInfo):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    number_of_items = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = "stock"
        verbose_name_plural = "stock"
        unique_together = ("product", "country")


class Country(CommonInfo):
    code = models.CharField(
        max_length=5, unique=True, blank=False, null=False, db_index=True
    )
    name = models.CharField(max_length=150, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"
