import textwrap

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse

from apps_dir.product.models import Product, Country, Stock


class ProductViewTest(TestCase):
    def setUp(self) -> None:
        super(ProductViewTest, self).setUp()

    def upload_csv(self, csv_content):
        # given that we have a few products already uploaded
        resp = self.client.put(
            path=reverse("products"),
            data=encode_multipart(
                data={
                    "file": SimpleUploadedFile(
                        "file_1.csv",
                        csv_content.strip().encode("utf-8"),
                        content_type="text/csv",
                    )
                },
                boundary=BOUNDARY,
            ),
            content_type=MULTIPART_CONTENT,
        )

        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_that_a_csv_file_can_be_imported(self):
        csv_content = textwrap.dedent(
            """
                country,sku,name,stock_change
                "dz","e920c573f128","Ramirez-Molina Granite Pizza","32"
                "gh","e920c573f128","Ramirez-Molina Granite Pizza","51"
                "ma","e920c573f128","Ramirez-Molina Granite Pizza","58"
                "ug","e920c573f128","Ramirez-Molina Granite Pizza","63"
                "dz","cbf87a9be799","Foster-Harrell Table","47"
                "eg","cbf87a9be799","Foster-Harrell Table","35"
                "ke","cbf87a9be799","Foster-Harrell Table","5"
                "ma","cbf87a9be799","Foster-Harrell Table","56"
                "ng","cbf87a9be799","Foster-Harrell Table","29"
                "ug","cbf87a9be799","Foster-Harrell Table","53"
                "dz","fb4d42219274","Christian, Santos and Campbell Refined Frozen Car","45"
                "gh","fb4d42219274","Christian, Santos and Campbell Refined Frozen Car","83"
                "ke","fb4d42219274","Christian, Santos and Campbell Refined Frozen Car","47"
                "ng","fb4d42219274","Christian, Santos and Campbell Refined Frozen Car","76"
                "ug","fb4d42219274","Christian, Santos and Campbell Refined Frozen Car","11"
                "ci","041f4e51a824","Lowe, Higgins and Cooley Ergonomic Wooden Pizza","51"
                "gh","041f4e51a824","Lowe, Higgins and Cooley Ergonomic Wooden Pizza","24"
                "ma","041f4e51a824","Lowe, Higgins and Cooley Ergonomic Wooden Pizza","89"
                "ng","041f4e51a824","Lowe, Higgins and Cooley Ergonomic Wooden Pizza","43"
                "ci","25461d1b1653","Golden-Wright Tasty Wooden Fish","48"
                "dz","25461d1b1653","Golden-Wright Tasty Wooden Fish","21"
                "gh","25461d1b1653","Golden-Wright Tasty Wooden Fish","14"
                "eg","59648d3c5d6e","Ali, Thompson and Eaton Ball","54"
                "gh","59648d3c5d6e","Ali, Thompson and Eaton Ball","19"
                "ke","23f8f2dd3842","Black-Campbell Used Concrete Bike","64"
                "ma","23f8f2dd3842","Black-Campbell Used Concrete Bike","72"
                "ng","23f8f2dd3842","Black-Campbell Used Concrete Bike","4"
                "ug","23f8f2dd3842","Black-Campbell Used Concrete Bike","64"
                "ci","e099ceaacfbe","Gutierrez and Sons For repair Steel Car","65"
                "eg","e099ceaacfbe","Gutierrez and Sons For repair Steel Car","27"
            """
        )

        # given that we have no products or stock set up
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(Stock.objects.count(), 0)

        # but we have the countries set up
        self.assertEqual(Country.objects.count(), 249)

        # When we upload a CSV file
        self.upload_csv(csv_content)

        # then we should have new products set up
        self.assertEqual(Product.objects.count(), 8)
        self.assertEqual(Stock.objects.count(), 30)

    def test_get_product_by_id(self):
        # Given that we have these items in store
        csv_content = textwrap.dedent(
            """
                country,sku,name,stock_change
                "dz","e920c573f128","Ramirez-Molina Granite Pizza","32"
                "gh","e920c573f128","Ramirez-Molina Granite Pizza","51"
                "ke","e920c573f128","Ramirez-Molina Granite Pizza","58"
                "ug","e920c573f128","Ramirez-Molina Granite Pizza","63"
            """
        )
        # When we upload a CSV file
        self.upload_csv(csv_content)

        product = Product.objects.last()
        resp = self.client.get(path=reverse("product", kwargs={"sku": product.sku}))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), {"sku": product.sku, "name": product.name})

    def test_that_stock_can_be_consumed(self):
        # Given that we have some stock
        csv_content = textwrap.dedent(
            """
                country,sku,name,stock_change
                "dz","e920c573f128","Ramirez-Molina Granite Pizza","32"
                "gh","e920c573f128","Ramirez-Molina Granite Pizza","51"
                "ma","e920c573f128","Ramirez-Molina Granite Pizza","58"
                "ug","e920c573f128","Ramirez-Molina Granite Pizza","63"
                "dz","cbf87a9be799","Foster-Harrell Table","47"
                "eg","cbf87a9be799","Foster-Harrell Table","35"
                "ke","cbf87a9be799","Foster-Harrell Table","5"
                "ma","cbf87a9be799","Foster-Harrell Table","56"
                "ng","cbf87a9be799","Foster-Harrell Table","29"
            """
        )
        self.upload_csv(csv_content)
        self.assertEqual(Product.objects.count(), 2)

        # When we consume a product
        resp = self.client.post(
            path=f"{reverse('consume-product', kwargs={'sku': 'cbf87a9be799', 'country_code': 'ke'})}?required_count=5"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # then we should have 0 items left
        self.assertEqual(
            Stock.objects.filter(product__sku="sku", country__code="KE").count(), 0
        )

        # and if we try again then we should indeed not have any mire stock left
        resp = self.client.post(
            path=f"{reverse('consume-product', kwargs={'sku': 'cbf87a9be799', 'country_code': 'ke'})}?required_count=5"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @parameterized.expand(
        [
            (
                textwrap.dedent(
                    """
                        country,sku,name,stock_change
                        "dz","e920c573f128","Ramirez-Molina Granite Pizza","32"
                        "gh","e920c573f128","Ramirez-Molina Granite Pizza","51"
                        "ke","e920c573f128","Ramirez-Molina Granite Pizza","58"
                        "ug","e920c573f128","Ramirez-Molina Granite Pizza","63"
                    """
                ),
                1,
                4,
                "e920c573f128",
                "ke",
                58,
            ),
            (
                textwrap.dedent(
                    """
                        country,sku,name,stock_change
                        "dz","e920c573f128","Ramirez-Molina Granite Pizza","32"
                        "gh","e920c573f128","Ramirez-Molina Granite Pizza","51"
                        "ke","e920c573f128","Ramirez-Molina Granite Pizza","58"
                        "ke","e920c573f128","Ramirez-Molina Granite Pizza","-5"
                        "ug","e920c573f128","Ramirez-Molina Granite Pizza","63"
                    """
                ),
                1,
                4,
                "e920c573f128",
                "ke",
                53,  # 58 - 5 == 53
            ),
            (
                textwrap.dedent(
                    """
                        country,sku,name,stock_change
                        "dz","e920c573f128","Ramirez-Molina Granite Pizza","32"
                        "gh","e920c573f128","Ramirez-Molina Granite Pizza","51"
                        "ke","e920c573f128","Ramirez-Molina Granite Pizza","58"
                        "ke","e920c573f129","Ramirez-Molina Granite Pizza hut","5"
                        "ug","e920c573f128","Ramirez-Molina Granite Pizza","63"
                    """
                ),
                2,
                5,
                "e920c573f129",
                "ke",
                5,
            ),
        ]
    )
    def test_product_updates(
        self,
        csv_content,
        products_count,
        stock_count,
        sku,
        country_code,
        number_of_items_in_country,
    ):
        # Given that we have these items in store
        self.upload_csv(csv_content)

        # Then we should have the right number of items
        self.assertEqual(Product.objects.count(), products_count)
        self.assertEqual(Stock.objects.count(), stock_count)

        self.assertEqual(
            Stock.objects.get(
                product__sku=sku, country__code=country_code.upper()
            ).number_of_items,
            number_of_items_in_country,
        )
