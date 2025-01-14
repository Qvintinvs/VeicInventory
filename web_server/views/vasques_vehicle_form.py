from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import AnyOf, DataRequired, Length, NumberRange


class VasquesVehicleForm(FlaskForm):
    year = IntegerField(
        "Year",
        validators=(
            DataRequired(message="Year is required."),
            NumberRange(
                min=1886, max=2100, message="Year must be between 1886 and 2100."
            ),
        ),
    )

    fuel = StringField(
        "Fuel",
        validators=(
            DataRequired(message="Fuel type is required."),
            Length(max=50, message="Fuel type must not exceed 50 characters."),
            AnyOf(
                values=("Gasoline", "Diesel", "Electric", "Hybrid"),
                message="Fuel type must be one of: Gasoline, Diesel, Electric, or Hybrid.",
            ),
        ),
    )

    subcategory = SelectField(
        "Subcategory",
        choices=(("A", "Type A"), ("B", "Type B"), ("C", "Type C")),
        validators=(
            DataRequired(message="Subcategory is required."),
            AnyOf(values=("A", "B", "C"), message="Subcategory must be A, B, or C."),
        ),
    )

    submit = SubmitField("Submit")
