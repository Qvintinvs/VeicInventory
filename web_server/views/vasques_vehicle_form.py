from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
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
            ("", "Selecione a subcategoria de CNH..."),
            ("A", "A - Motos, motonetas e triciclos"),
            ("B", "B - Carros de passeio, utilitário/SUV, minivan, picape"),
            ("C", "C - Caminhões, caminhonetes, vans de carga"),
            ("D", "D - Ônibus, microônibus, vans de passageiros"),
            ("E", "E - Veículos pesados"),
        ),
        validators=(DataRequired(), AnyOf(values=("A", "B", "C", "D", "E"))),
    )

    submit = SubmitField("Salvar")
