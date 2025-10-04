from django.test import TestCase


class WRFEmissionTests(TestCase):
    """
    WRFStandardEmission examples:

    emission_with_subcategory_properties = WRFStandardEmission.objects.create(
        subcategory_name=CNHChoices.E,
        fuel="Gasoline",
        fraction=0.5,
        mileage=1000,
    )
    """
