from typing import cast

from flask_wtf import FlaskForm
from models.wrf_standard_emission import WRFStandardEmission
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import AnyOf, DataRequired, Length, NumberRange, Optional

from .subcategory_field import SubcategoryField


class WRFStandardEmissionForm(FlaskForm):
    fuel = StringField(
        validators=(
            DataRequired(),
            AnyOf(("Gasoline", "Alcohol", "Diesel", "Electric", "Flex")),
        )
    )

    subcategory = SubcategoryField()

    fraction = FloatField(
        "Fração do Veículo na frota:",
        render_kw={"placeholder": "Ex: 15 (%)"},
        validators=(DataRequired(), NumberRange(min=0)),
    )

    mileage = FloatField(
        "Quilometragem do veículo (km/dia):",
        render_kw={"placeholder": "Ex: 12.5 (km/dia)"},
        validators=(DataRequired(), NumberRange(min=0)),
    )

    note = StringField(
        "Nota do veículo:",
        render_kw={"placeholder": "Ex: Taxi"},
        validators=(Optional(), Length(max=256)),
    )

    submit = SubmitField("Salvar")

    @property
    def vehicle(self):
        return WRFStandardEmission(
            cast(str, self.fuel.data),
            self.subcategory.cnh_subcategory,
            cast(float, self.fraction.data),
            cast(float, self.mileage.data) / 100,
            cast(str, self.note.data),
        )
