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
    name = models.CharField(max_length=150)
