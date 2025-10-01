from django.test import TestCase

from .models import WRFStandardEmission
from .models.cnh_subcategory import CNHSubcategory


class WRFEmissionTests(TestCase):
    def test_create_emission(self):
        example_subcategory = CNHSubcategory.E

        emission = WRFStandardEmission(
            fuel="Gasoline",
            subcategory=example_subcategory,
            fraction=0.1,
            mileage=10000,
        )

        emission.save()

        self.assertEqual(emission.subcategory, example_subcategory.value)
