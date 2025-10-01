from django.test import TestCase

from .models import WRFStandardEmission
from .models.cnh_subcategory import CNHSubcategory


class WRFEmissionTests(TestCase):
    def test_subcategory_getter_returns_correct_object(self):
        emission_with_subcategory_properties = WRFStandardEmission.objects.create(
            subcategory_name="Lightweight",
            subcategory_deterioration_factor=1.2,
            subcategory_category_consumption=10.5,
            fuel="Gasoline",
            fraction=0.5,
            mileage=1000,
        )
        emission_subcategory = emission_with_subcategory_properties.subcategory

        self.assertEqual(emission_subcategory.name, "Lightweight")
        self.assertEqual(emission_subcategory.deterioration_factor, 1.2)
        self.assertEqual(emission_subcategory.category_consumption, 10.5)

    def test_subcategory_setter_updates_model_fields(self):
        emission_to_be_setted = WRFStandardEmission(
            fuel="Gasoline", fraction=0.5, mileage=1000
        )
        emission_to_be_setted.subcategory = CNHSubcategory.A

        self.assertEqual(
            emission_to_be_setted.subcategory_name, CNHSubcategory.A.value.name
        )
        self.assertEqual(
            emission_to_be_setted.subcategory_deterioration_factor,
            CNHSubcategory.A.value.deterioration_factor,
        )
        self.assertEqual(
            emission_to_be_setted.subcategory_category_consumption,
            CNHSubcategory.A.value.category_consumption,
        )
