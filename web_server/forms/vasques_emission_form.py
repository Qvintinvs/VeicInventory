from typing import cast

from flask_wtf import FlaskForm
from models.city import City
from models.vasques_emission_model import VasquesEmissionModel
from wtforms import FloatField, IntegerField, StringField
from wtforms.validators import AnyOf, DataRequired, NumberRange

from .subcategory_field import SubcategoryField


class VasquesEmissionForm(FlaskForm):
    year = IntegerField(validators=(DataRequired(), NumberRange(1886, 2100)))

    fuel = StringField(
        validators=(
            DataRequired(),
            AnyOf(("Gasoline", "Alcohol", "Diesel", "Electric", "Flex")),
        )
    )

    subcategory = SubcategoryField()

    exhaust_emission_factor = FloatField(
        validators=(DataRequired(), NumberRange(min=0))
    )

    autonomy = FloatField(validators=(DataRequired(), NumberRange(min=0)))

    @property
    def vehicle_emission(self):
        example_city = City("Itajaí", 1.1)

        return VasquesEmissionModel(
            cast(int, self.year.data),
            cast(str, self.fuel.data),
            self.subcategory.cnh_subcategory,
            cast(float, self.exhaust_emission_factor.data),
            cast(float, self.autonomy.data),
            example_city,
        )
