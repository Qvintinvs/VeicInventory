from typing import cast

from flask_wtf import FlaskForm
from models.city import City
from models.vasques_emission_model import VasquesEmissionModel
from wtforms import FloatField, IntegerField, SelectField, SubmitField, StringField
from wtforms.validators import AnyOf, DataRequired, NumberRange, Optional, Length

from .subcategory_field import SubcategoryField


class VasquesVehicleForm(FlaskForm):
    # year = IntegerField(
    #     "Ano:",
    #     render_kw={"placeholder": "Ex: 2024"},
    #     validators=(DataRequired(), NumberRange(min=1886, max=2100)),
    # )

    fraction = FloatField(
        "Fração do Veículo na frota:",
        render_kw={"placeholder": "Ex: 15 (%)"},
        validators=(DataRequired(), NumberRange(min=0)),
    )

    fuel = SelectField(
        "Combustível:",
        choices=(
            ("", "Selecione..."),
            ("Gasolina", "Gasolina"),
            ("Álcool", "Álcool"),
            ("Flex", "Flex"),
            ("Diesel", "Diesel"),
            ("Elétrico", "Elétrico"),
        ),
        validators=(
            DataRequired(),
            AnyOf(("Gasolina", "Álcool",  "Flex", "Diesel", "Elétrico")),
        ),
    )

    subcategory = SubcategoryField()

    # exhaust_emission_factor = FloatField(
    #     "Fator de Emissão por Exaustão:",
    #     render_kw={"placeholder": "Ex: 0.25 (g/km)"},
    #     validators=(DataRequired(), NumberRange(min=0)),
    # )

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
        example_city = City("Itajaí", 1.1)

        return VasquesEmissionModel(
            # cast(int, self.year.data),
            cast(str, self.fuel.data),
            self.subcategory.cnh_subcategory,
            # cast(float, self.exhaust_emission_factor.data),
            cast(float, self.mileage.data),
            cast(float, self.fraction.data/100),
            cast(str, self.note.data),
            example_city,
        )
