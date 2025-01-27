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
            AnyOf(("Gasolina", "Álcool", "Diesel", "Elétrico", "Flex")),
        ),
    )

    subcategory = SelectField(
        "Subcategoria:",
        choices=(
            ("", "Selecione a subcategoria de CNH..."),
            ("A", "A - Motos, motonetas e triciclos"),
            ("B", "B - Carros de passeio, utilitário/SUV, minivan, picape"),
            ("C", "C - Caminhões, caminhonetes, vans de carga"),
            ("D", "D - Ônibus, microônibus, vans de passageiros"),
            ("E", "E - Veículos pesados"),
        ),
        validators=(
            DataRequired(),
            AnyOf(("A", "B", "C", "D", "E")),
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
    def vehicle_subcategory(self):
        form_value: str | None = self.subcategory.data

        matches_in_the_cnh_subcategories = (
            subcategory.value
            for subcategory in CNHSubcategory
            if subcategory.name == form_value
        )

        subcategory_of_the_value = next(matches_in_the_cnh_subcategories, None)

        if subcategory_of_the_value is None:
            raise ValueError(f"Invalid value for CNHSubcategory: {form_value}")

        return subcategory_of_the_value

    @property
    def vehicle(self):
        example_city = City("Itajaí", 1.1)

        return VasquesVehicleModel(
            cast(int, self.year.data),
            cast(str, self.fuel.data),
            self.vehicle_subcategory,
            cast(float, self.exhaust_emission_factor.data),
            cast(float, self.autonomy.data),
            example_city,
        )
