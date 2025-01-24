from typing import cast

from flask_wtf import FlaskForm
from models.city import City
from models.cnh_subcategory import CNHSubcategory
from models.vasques_vehicle_model import VasquesVehicleModel
from wtforms import FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import AnyOf, DataRequired, NumberRange


class VasquesVehicleForm(FlaskForm):
    year = IntegerField(
        "Ano:",
        render_kw={"placeholder": "Ex: 2024"},
        validators=(DataRequired(), NumberRange(min=1886, max=2100)),
    )

    fuel = SelectField(
        "Combustível:",
        choices=(
            ("", "Selecione..."),
            ("Gasolina", "Gasolina"),
            ("Álcool", "Álcool"),
            ("Diesel", "Diesel"),
            ("Elétrico", "Elétrico"),
            ("Flex", "Flex"),
        ),
        validators=(
            DataRequired(),
            AnyOf(values=("Gasolina", "Álcool", "Diesel", "Elétrico", "Flex")),
        ),
    )

    subcategory = SelectField(
        "Subcategoria:",
        choices=(
            (None, "Selecione a subcategoria de CNH..."),
            (CNHSubcategory.A, "A - Motos, motonetas e triciclos"),
            (
                CNHSubcategory.B,
                "B - Carros de passeio, utilitário/SUV, minivan, picape",
            ),
            (CNHSubcategory.C, "C - Caminhões, caminhonetes, vans de carga"),
            (CNHSubcategory.D, "D - Ônibus, microônibus, vans de passageiros"),
            (CNHSubcategory.E, "E - Veículos pesados"),
        ),
        validators=(
            DataRequired(),
            AnyOf(values=tuple(subcategory.value for subcategory in CNHSubcategory)),
        ),
    )

    exhaust_emission_factor = FloatField(
        "Fator de Emissão por Exaustão:",
        render_kw={"placeholder": "Ex: 0.25 (g/km)"},
        validators=(DataRequired(), NumberRange(min=0)),
    )

    autonomy = FloatField(
        "Autonomia do Veículo (km/L ou km/kWh):",
        render_kw={"placeholder": "Ex: 12.5 (km/L)"},
        validators=(DataRequired(), NumberRange(min=0)),
    )

    submit = SubmitField("Salvar")

    @property
    def vehicle(self):
        example_city = City("Itajaí", 1.1)

        return VasquesVehicleModel(
            cast(int, self.year.data),
            cast(str, self.fuel.data),
            cast(CNHSubcategory, self.subcategory.data),
            cast(float, self.exhaust_emission_factor.data),
            cast(float, self.autonomy.data),
            example_city,
        )
